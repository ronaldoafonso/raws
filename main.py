
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

    pub_subnet = Subnet()
    pub_subnet.create('10.0.0.0/24', vpc.get_id())
    pub_subnet.tag('Name', 'ra-pub-subnet')
    pub_rt = RouteTable()
    pub_rt.create(vpc.get_id())
    pub_rt.tag('Name', 'ra-pub-routetable')
    pub_rt.add_route(igw.get_id(), '0.0.0.0/0')
    pub_assoc = Association()
    pub_assoc.assoc_route_table_with_subnet(pub_rt.get_id(), pub_subnet.get_id())

    priv_subnet = Subnet()
    priv_subnet.create('10.0.1.0/24', vpc.get_id(), public=False)
    priv_subnet.tag('Name', 'ra-priv-subnet')
    priv_rt = RouteTable()
    priv_rt.create(vpc.get_id())
    priv_rt.tag('Name', 'ra-priv-routetable')
    priv_assoc = Association()
    priv_assoc.assoc_route_table_with_subnet(priv_rt.get_id(), priv_subnet.get_id())

    dummy = input('Waiting')

    priv_assoc.disassoc_route_table_with_subnet()
    priv_rt.delete()
    priv_subnet.delete()

    pub_assoc.disassoc_route_table_with_subnet()
    pub_rt.delete()
    pub_subnet.delete()
    igw.detach_from_vpc(vpc.get_id())
    igw.delete()

    vpc.delete()


if __name__ == '__main__':
    main()
