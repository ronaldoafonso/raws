from .aws import Aws


class EC2(Aws):

    USER_DATA = """
#!/bin/bash
yum install httpd -y
systemctl start httpd
systemctl enable httpd
"""

    def __init__(self, key_name, security_group_ids, subnet_id):
        self.key_name = key_name
        self.security_group_ids = security_group_ids
        self.subnet_id = subnet_id
        super().__init__()

    def launch(self):
        instances = self.aws.run_instances(
            ImageId='ami-0096398577720a4a3',
            KeyName=self.key_name,
            MinCount=1,
            MaxCount=1,
            InstanceType='t2.micro',
            SecurityGroupIds=self.security_group_ids,
            SubnetId=self.subnet_id,
            UserData=EC2.USER_DATA
        )
        self.resource_id = [instance['InstanceId']
                            for instance in instances['Instances']]

    def terminate(self):
        waiter = self.aws.get_waiter('instance_terminated')
        self.aws.terminate_instances(InstanceIds=self.get_id())
        waiter.wait(InstanceIds=self.get_id())
