
import boto3


class Client:

    def __init__(self):
        self._client = boto3.client('ec2')

    def create_vpc(self, cidr_block):
        vpc = self._client.create_vpc(CidrBlock=cidr_block)
        self.vpc_id = vpc['Vpc']['VpcId']
        return vpc

    def add_name_tag(self, name):
        return self._client.create_tags(
                Resources=[self.vpc_id],
                Tags=[
                    {'Key': 'Name', 'Value': name}
                ]
        )

    def create_internet_gateway(self):
        igw = self._client.create_internet_gateway()
        self.igw_id = igw['InternetGateway']['InternetGatewayId']
        self._client.create_tags(
                Resources=[self.igw_id],
                Tags=[
                    {'Key': 'Name', 'Value': 'ra-igw'}
                ]
        )
        return self._client.attach_internet_gateway(InternetGatewayId=self.igw_id,
                                                    VpcId=self.vpc_id)

    def create_pubsub(self, cidr_block):
        subnet = self._client.create_subnet(CidrBlock=cidr_block, VpcId=self.vpc_id)
        self.pub_subnet_id = subnet['Subnet']['SubnetId']
        self._client.create_tags(
                Resources=[self.pub_subnet_id],
                Tags=[
                    {'Key': 'Name', 'Value': 'ra-pub-subnet'}
                ]
        )
        self._client.modify_subnet_attribute(
            MapPublicIpOnLaunch={'Value': True},
            SubnetId=self.pub_subnet_id,
        )
        return subnet

    def create_pub_routetable(self):
        routetable = self._client.create_route_table(VpcId=self.vpc_id)
        self.pub_routetable_id = routetable['RouteTable']['RouteTableId']
        self._client.create_tags(
                Resources=[self.pub_routetable_id],
                Tags=[
                    {'Key': 'Name', 'Value': 'ra-pub-routetable'}
                ]
        )
        self._client.create_route(RouteTableId=self.pub_routetable_id,
                                  GatewayId=self.igw_id,
                                  DestinationCidrBlock='0.0.0.0/0')
        return routetable

    def associate_route_table(self):
        assoc_pub_route_table = self._client.associate_route_table(RouteTableId=self.pub_routetable_id,
                                                                   SubnetId=self.pub_subnet_id)
        self.assoc_pub_route_id = assoc_pub_route_table['AssociationId']
        return assoc_pub_route_table

    def disassociate_route_table(self):
        self._client.disassociate_route_table(AssociationId=self.assoc_pub_route_id)

    def delete_pub_routetable(self):
        self._client.delete_route_table(RouteTableId=self.pub_routetable_id)

    def delete_pubsub(self):
        self._client.delete_subnet(SubnetId=self.pub_subnet_id)

    def delete_internet_gateway(self):
        self._client.detach_internet_gateway(InternetGatewayId=self.igw_id,
                                             VpcId=self.vpc_id)
        self._client.delete_internet_gateway(InternetGatewayId=self.igw_id)

    def delete_vpc(self):
        return self._client.delete_vpc(VpcId=self.vpc_id)
