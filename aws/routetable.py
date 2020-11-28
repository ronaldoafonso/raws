
from .aws import Aws


class RouteTable(Aws):

    def __init__(self, vpc_id):
        self.vpc_id = vpc_id
        super().__init__()

    def create(self):
        routetable = self.aws.create_route_table(VpcId=self.vpc_id)
        self.resource_id = routetable['RouteTable']['RouteTableId']

    def add_route(self, igw_id, dest_cidr_block):
        self.aws.create_route(
            RouteTableId=self.get_id(),
            GatewayId=igw_id,
            DestinationCidrBlock=dest_cidr_block
        )

    def delete(self):
        self.aws.delete_route_table(RouteTableId=self.get_id())


class Association(Aws):

    def assoc_route_table_with_subnet(self, routetable_id, subnet_id):
        association = self.aws.associate_route_table(
            RouteTableId=routetable_id,
            SubnetId=subnet_id
        )
        self.resource_id = association['AssociationId']

    def disassoc_route_table_with_subnet(self):
        self.aws.disassociate_route_table(
                AssociationId=self.get_id()
        )
