
from aws import Aws


class Igw(Aws):

    def create(self):
        igw = self.aws.create_internet_gateway()
        self.resource_id = igw['InternetGateway']['InternetGatewayId']

    def attach_to_vpc(self, vpc_id):
        self.aws.attach_internet_gateway(
            InternetGatewayId=self.get_id(),
            VpcId=vpc_id
        )

    def detach_from_vpc(self, vpc_id):
        self.aws.detach_internet_gateway(
            InternetGatewayId=self.get_id(),
            VpcId=vpc_id
        )

    def delete(self):
        self.aws.delete_internet_gateway(InternetGatewayId=self.get_id())
