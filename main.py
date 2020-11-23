
import time

from client import Client


def main():
    client = Client()
    vpc = client.create_vpc('10.0.0.0/16')
    print(f'VPC {vpc}.')
    rc_name_tag = client.add_name_tag('ra-vpc')
    print(f'VPC tag name: {rc_name_tag}.')
    rc_igw = client.create_internet_gateway()
    print(f'Internet Gateway: {rc_igw}.')

    time.sleep(30)

    client.delete_internet_gateway()
    rc_delete_vpc = client.delete_vpc()
    print(f'Delete VPC: {rc_delete_vpc}.')


if __name__ == '__main__':
    main()
