
import boto3


class Aws:

    def __init__(self):
        self.aws = boto3.client('ec2')

    def get_id(self):
        return self.resource_id

    def tag(self, key, value):
        self.aws.create_tags(
            Resources=[self.get_id()],
            Tags=[{'Key': key, 'Value': value}]
        )
