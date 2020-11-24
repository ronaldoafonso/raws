
import boto3


class Client:

    def __init__(self):
        self.client = boto3.client('ec2')

    def get_id(self):
        return self.resource_id

    def tag(self, key, value):
        self.client.create_tags(
            Resources=[self.get_id()],
            Tags=[{'Key': key, 'Value': value}]
        )


class Vpc(Client):

    def create(self, cidr_block):
        vpc = self.client.create_vpc(CidrBlock=cidr_block)
        self.resource_id = vpc['Vpc']['VpcId']

    def delete(self):
        return self.client.delete_vpc(VpcId=self.get_id())


class Igw(Client):

    def create(self):
        igw = self.client.create_internet_gateway()
        self.resource_id = igw['InternetGateway']['InternetGatewayId']

    def delete(self):
        self.client.delete_internet_gateway(InternetGatewayId=self.get_id())
