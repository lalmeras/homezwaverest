from openzwave.network import ZWaveNetwork
from openzwave.node import ZWaveNode
from openzwave.value import ZWaveValue


class RestNetwork(object):
    def __init__(self, network):
        assert isinstance(network, ZWaveNetwork)
        self.network = network

    def __json__(self, request):
        return dict(
            state=self.network.state
        )


class RestNode(object):
    def __init__(self, node):
        assert isinstance(node, ZWaveNode)
        self.node = node

    def __json__(self, request):
        return dict(
            home_id=self.node.home_id,
            node_id=self.node.node_id,
            name=self.node.name,
            product=RestProduct(self.node),
            location=self.node.location,
        )


class RestNodeValue(object):
    def __init__(self, value):
        assert isinstance(value, ZWaveValue)
        self.value = value

    def __json__(self, request):
        return dict(
            command_class=self.value.command_class,
            index=self.value.index,
            label=self.value.label,
            help=self.value.help,
            data=self.value.data_as_string,
            value_id=self.value.value_id,
            type=self.value.type,
            units=self.value.units
        )


class RestProduct(object):
    def __init__(self, node):
        self.node = node

    def __json__(self, request):
        return dict(
            product_id=self.node.product_id,
            name=self.node.product_name,
            type=self.node.product_type
        )