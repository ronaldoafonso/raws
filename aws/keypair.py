
import os

from .aws import Aws


class KeyPair(Aws):

    def __init__(self, name):
        self.name = name
        super().__init__()

    def get_name(self):
        return self.name

    def create(self):
        keypair = self.aws.create_key_pair(KeyName=self.name)
        self.resource_id = keypair['KeyPairId']
        self.path = f'/home/ronaldo/.ssh/aws/{self.get_id()}'
        with open(self.path, 'w+') as fd:
            fd.write(keypair['KeyMaterial'])
        os.chmod(self.path, 0o0600)

    def delete(self):
        self.aws.delete_key_pair(KeyPairId=self.get_id())
        os.remove(self.path)
