
import boto3


def Client():
    return boto3.client('ec2')


class Vpc:

    def __init__(self, client):
        self.client = client
        self.vpc_id = None

    def create(self, cidr_block):
        vpc = self.client.create_vpc(CidrBlock=cidr_block)
        self.vpc_id = vpc['Vpc']['VpcId']

    def delete(self):
        return self.client.delete_vpc(VpcId=self.vpc_id)

    def tag(self, key, value):
        self.client.create_tags(
            Resources=[self.vpc_id],
            Tags=[{'Key': key, 'Value': value}]
        )
