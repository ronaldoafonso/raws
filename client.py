
import boto3


class Client:

    def __init__(self):
        self._client = boto3.client('ec2')

    def create_vpc(self, cidr_block):
        vpc = self._client.create_vpc(CidrBlock=cidr_block)
        self.vpc_id = vpc['Vpc']['VpcId']
        return vpc

    def add_name_tag(self, name):
        return self._client.create_tags(
                Resources=[self.vpc_id],
                Tags=[
                    {'Key': 'Name', 'Value': name}
                ]
        )

    def create_internet_gateway(self):
        igw = self._client.create_internet_gateway()
        self.igw_id = igw['InternetGateway']['InternetGatewayId']
        self._client.create_tags(
                Resources=[self.igw_id],
                Tags=[
                    {'Key': 'Name', 'Value': 'ra-igw'}
                ]
        )
        return self._client.attach_internet_gateway(InternetGatewayId=self.igw_id,
                                                    VpcId=self.vpc_id)

    def delete_internet_gateway(self):
        self._client.detach_internet_gateway(InternetGatewayId=self.igw_id,
                                             VpcId=self.vpc_id)
        self._client.delete_internet_gateway(InternetGatewayId=self.igw_id)

    def delete_vpc(self):
        return self._client.delete_vpc(VpcId=self.vpc_id)
