from rest_toolkit import quick_serve
from rest_toolkit import resource

from homezwaverest.zwave import *

class RestProduct(object):
    def __init__(self, node):
        self.node = node
    
    def __json__(self, request):
        return dict(
            product_id=self.node.product_id,
            name=self.node.product_name,
            type=self.node.product_type
        )

class RestNode(object):
    def __init__(self, node):
        self.node = node

    def __json__(self, request):
        return dict(
            home_id=self.node.home_id,
            node_id=self.node.node_id,
            name=self.node.name,
            product=RestProduct(self.node)
        )

class RestValue(object):
    def __init__(self, value):
        return dict(
            command_class=value.command_class,
            index=value.index,
            label=value.label,
            help=value.help,
            data=value.data,
            value_id=value.alue_id,
            type=value.type,
            units=value.units,
        )

@resource('/')
class Root(object):
    def __init__(self, request):
        pass

@resource('/network/state/')
class NetworkState(object):
    def __init__(self, request):
        pass

@NetworkState.GET()
def get_network_state(resource, request):
    return network.state

@resource('/nodes/')
class Nodes(object):
    def __init__(self, request):
        self.nodes = network.nodes

@resource('/node/{id}/')
class Node(object):
    def __init__(self, request):
        id = request.matchdict['id']
        self.node = network.nodes[int(id)]

@resource('/node/{id}/values/')
class NodeValues(object):
    def __init__(self, request):
        id = request.matchdict['id']
        self.node = network.nodes[int(id)]

@Nodes.GET()
def get_nods(resource, request):
    return [RestNode(node) for node in resource.nodes]

@Node.GET()
def get_node(resource, request):
    return RestNode(resource.node)

@NodeValues.GET()
def get_node_values(resource, request):
    return [RestValue(value) for value_id, value in resource.node.get_values()]

@Root.GET()
def show_root(root, request):
    return {'status': 'OK'}

def main():
    quick_serve()

if __name__ == '__main__':
    quick_serve()
