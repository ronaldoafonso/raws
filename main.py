
from client import Client


def main():
    client = Client()
    vpc = client.create_vpc('10.0.0.0/16')
    print(f'VPC {vpc}.')
    rc_name_tag = client.add_name_tag('ra-vpc')
    print(f'VPC tag name: {rc_name_tag}.')
    rc_igw = client.create_internet_gateway()
    print(f'Internet Gateway: {rc_igw}.')
    rc_pubsub = client.create_pubsub('10.0.0.0/24')
    print(f'Public subnet: {rc_pubsub}.')
    rc_pub_routetable = client.create_pub_routetable()
    print(f'Public route table: {rc_pub_routetable}.')
    rc_assoc_pub_routetable = client.associate_route_table()
    print(f'Associate route table: {rc_assoc_pub_routetable}.')

    dummy = input('Waiting')

    client.disassociate_route_table()
    client.delete_pub_routetable()
    client.delete_pubsub()
    client.delete_internet_gateway()
    rc_delete_vpc = client.delete_vpc()
    print(f'Delete VPC: {rc_delete_vpc}.')


if __name__ == '__main__':
    main()
