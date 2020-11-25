
from .aws import Aws


class KeyPair(Aws):

    def __init__(self, name):
        self.name = name
        super().__init__()

    def create(self):
        keypair = self.aws.create_key_pair(KeyName=self.name)
        self.resource_id = keypair['KeyPairId']

    def delete(self):
        self.aws.delete_key_pair(KeyPairId=self.get_id())
