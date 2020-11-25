
from .aws import Aws


IP_PERMISSIONS = {
    'ssh': {
        'IpProtocol': 'tcp',
        'FromPort': 22,
        'ToPort': 22,
        'IpRanges': [
            {
                'CidrIp': '0.0.0.0/0',
                'Description': 'All IPs'
            }
        ]
    },
    'http': {
        'IpProtocol': 'tcp',
        'FromPort': 80,
        'ToPort': 80,
        'IpRanges': [
            {
                'CidrIp': '0.0.0.0/0',
                'Description': 'All IPs'
            }
        ]
    }
}


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

    def add_ingress_rule(self):
        self.aws.authorize_security_group_ingress(
            GroupId=self.get_id(),
            IpPermissions=[
                IP_PERMISSIONS['ssh'],
                IP_PERMISSIONS['http']
            ]
        )

    def del_ingress_rule(self):
        self.aws.revoke_security_group_ingress(
            GroupId=self.get_id(),
            IpPermissions=[
                IP_PERMISSIONS['ssh'],
                IP_PERMISSIONS['http']
            ]
        )

    def delete(self):
        self.aws.delete_security_group(GroupId=self.get_id())
