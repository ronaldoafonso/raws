
from aws.vpc import Vpc
from aws.igw import Igw
from aws.subnet import Subnet
from aws.routetable import RouteTable, Association


def main():
    vpc = Vpc('10.0.0.0/16')
    vpc.create()
    vpc.tag('Name', 'ra-vpc')

    igw = Igw()
    igw.create()
    igw.tag('Name', 'ra-igw')
    igw.attach_to_vpc(vpc.get_id())

    pub_subnet = Subnet('10.0.0.0/24', vpc.get_id())
    pub_subnet.create()
    pub_subnet.tag('Name', 'ra-pub-subnet')
    pub_rt = RouteTable(vpc.get_id())
    pub_rt.create()
    pub_rt.tag('Name', 'ra-pub-routetable')
    pub_rt.add_route(igw.get_id(), '0.0.0.0/0')
    pub_assoc = Association()
    pub_assoc.assoc_route_table_with_subnet(pub_rt.get_id(), pub_subnet.get_id())

    priv_subnet = Subnet('10.0.1.0/24', vpc.get_id())
    priv_subnet.create(public=False)
    priv_subnet.tag('Name', 'ra-priv-subnet')
    priv_rt = RouteTable(vpc.get_id())
    priv_rt.create()
    priv_rt.tag('Name', 'ra-priv-routetable')
    priv_assoc = Association()
    priv_assoc.assoc_route_table_with_subnet(priv_rt.get_id(), priv_subnet.get_id())

    output = f'VPD id: {vpc.get_id()}.\n' + \
             f'PUB SUBNET id: {pub_subnet.get_id()}.\n' + \
             f'Waiting: \n\n'
    dummy = input(output)

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
