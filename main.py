
from vpc import Vpc
from igw import Igw
from subnet import Subnet
from routetable import RouteTable, Association


def main():
    vpc = Vpc()
    vpc.create('10.0.0.0/16')
    vpc.tag('Name', 'ra-vpc')

    igw = Igw()
    igw.create()
    igw.tag('Name', 'ra-igw')
    igw.attach_to_vpc(vpc.get_id())

    sub = Subnet(public=True)
    sub.create('10.0.0.0/24', vpc.get_id())
    sub.tag('Name', 'ra-pub-subnet')

    routetable = RouteTable()
    routetable.create(vpc.get_id())
    routetable.tag('Name', 'ra-pub-routetable')
    routetable.add_route(igw.get_id(), '0.0.0.0/0')

    assoc = Association()
    assoc.assoc_route_table_with_subnet(routetable.get_id(), sub.get_id())

    dummy = input('Waiting')

    assoc.disassoc_route_table_with_subnet()
    routetable.delete()
    sub.delete()
    igw.detach_from_vpc(vpc.get_id())
    igw.delete()
    vpc.delete()


if __name__ == '__main__':
    main()
