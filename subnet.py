
from aws import Aws


class Subnet(Aws):

    def create(self, cidr_block, vpc_id, public=True):
        subnet = self.aws.create_subnet(
                CidrBlock=cidr_block,
                VpcId=vpc_id
        )
        self.resource_id = subnet['Subnet']['SubnetId']
        if public:
            self.aws.modify_subnet_attribute(
                MapPublicIpOnLaunch={'Value': True},
                SubnetId=self.get_id(),
            )

    def delete(self):
        self.aws.delete_subnet(SubnetId=self.get_id())
