
from argparse import ArgumentParser

from aws.keypair import KeyPair
from aws.securitygroup import SecurityGroup
from aws.ec2 import EC2


def main(vpc_id, subnet_id):
    kp = KeyPair('ra-keypair')
    kp.create()

    sg = SecurityGroup('ra-sg', 'SSH and HTTP security group', vpc_id)
    sg.create()
    sg.add_ingress_rule()

    ec2 = EC2(kp.get_name(), [sg.get_id()], subnet_id)
    ec2.launch()

    dummy = input(f'Waiting: ')

    ec2.terminate()

    sg.del_ingress_rule()
    sg.delete()

    kp.delete()


if __name__ == '__main__':
    parser = ArgumentParser(prog='ec2', description='Lauch EC2 instances.')
    parser.add_argument('-v', '--vpcid', type=str, default='')
    parser.add_argument('-s', '--subid', type=str, default='')
    args = parser.parse_args()

    main(args.vpcid, args.subid)
