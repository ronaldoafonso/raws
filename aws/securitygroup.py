
from .aws import Aws


class SecurityGroup(Aws):

    def __init__(self, name, description, vpc_id):
        self.name = name
        self.description = description
        self.vpc_id = vpc_id
        super().__init__()

    def create(self):
        securitygroup = self.aws.create_security_group(
            GroupName=self.name,
            Description=self.description,
            VpcId=self.vpc_id
        )
        self.resource_id = securitygroup['GroupId']

    def delete(self):
        self.aws.delete_security_group(GroupId=self.get_id())
