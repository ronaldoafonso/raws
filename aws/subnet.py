
from .aws import Aws


class Subnet(Aws):

    def __init__(self, cidr_block, vpc_id):
        self.cidr_block = cidr_block
        self.vpc_id = vpc_id
        super().__init__()

    def create(self, public=True):
        subnet = self.aws.create_subnet(
                CidrBlock=self.cidr_block,
                VpcId=self.vpc_id
        )
        self.resource_id = subnet['Subnet']['SubnetId']
        if public:
            self.aws.modify_subnet_attribute(
                MapPublicIpOnLaunch={'Value': True},
                SubnetId=self.get_id(),
            )

    def delete(self):
        self.aws.delete_subnet(SubnetId=self.get_id())
