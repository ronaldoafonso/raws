
from .aws import Aws


class Vpc(Aws):

    def __init__(self, cidr_block):
        self.cidr_block = cidr_block
        super().__init__()

    def create(self):
        vpc = self.aws.create_vpc(CidrBlock=self.cidr_block)
        self.resource_id = vpc['Vpc']['VpcId']

    def delete(self):
        self.aws.delete_vpc(VpcId=self.get_id())
