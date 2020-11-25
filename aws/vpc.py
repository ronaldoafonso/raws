
from .aws import Aws


class Vpc(Aws):

    def create(self, cidr_block):
        vpc = self.aws.create_vpc(CidrBlock=cidr_block)
        self.resource_id = vpc['Vpc']['VpcId']

    def delete(self):
        return self.aws.delete_vpc(VpcId=self.get_id())
