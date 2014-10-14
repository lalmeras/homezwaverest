""" Cornice services.
"""

from cornice import Service
from cornice.resource import resource, view

from openzwave.network import ZWaveNetwork
from openzwave.node import ZWaveNode
from openzwave.value import ZWaveValue

from colander import Schema, SchemaNode, String, Int

from homezwaverest.model import RestNetwork, RestNode, RestNodeValue

node_values = Service(name='node-values', path='/node/{node_id}/values/')
node_value = Service(name='node-value', path='/node/{node_id}/value/{value_id}/')
node_value_data = Service(name='node-value-data', path='/node/{node_id}/value/{value_id}/{data}/')
node_value_index_data = Service(name='node-value-index-data',
                                path='/node/{node_id}/command_class/{command_class}/value/{index}/{data}/')

def includeme(config):
    """
    @type config: pyramid.config.Configurator
    """
    config.add_static_view(name='static', path='homezwaverest:static/')

class NodeIdSchema(Schema):
    node_id = SchemaNode(Int(), title='node_id', location='path')


class NodeIdValueIdSchema(NodeIdSchema):
    value_id = SchemaNode(Int(), title='value_id', location='path')


class NodeIdValueIdDataSchema(NodeIdValueIdSchema):
    data = SchemaNode(String(), title="data", location="path")


class NodeIdCommandClassValueIndexDataSchema(NodeIdSchema):
    command_class = SchemaNode(Int(), title="command_class", location="path")
    index = SchemaNode(Int(), title="index", location="path")
    data = SchemaNode(String(), title="data", location="path")

@node_values.get(schema=NodeIdSchema)
def get_node_values(request):
    network_provider = NetworkProvider(request.network)
    node_id = request.validated['node_id']
    return [RestNodeValue(value) for value in network_provider.get_node_values(node_id)]

@node_value.get(schema=NodeIdValueIdSchema)
def get_node_value(request):
    network_provider = NetworkProvider(request.network)
    node_id = request.validated['node_id']
    value_id = request.validated['value_id']
    return RestNodeValue(network_provider.get_node_value_by_id(node_id, value_id))

@node_value_data.put(schema=NodeIdValueIdDataSchema)
def put_node_value(request):
    network_provider = NetworkProvider(request.network)
    node_id = request.validated['node_id']
    value_id = request.validated['value_id']
    data = get_data(request.validated['data'])
    value = network_provider.get_node_value_by_id(node_id, value_id)
    value.data = data
    return RestNodeValue(value)

@node_value_index_data.put(schema=NodeIdCommandClassValueIndexDataSchema)
def put_node_value(request):
    network_provider = NetworkProvider(request.network)
    node_id = request.validated['node_id']
    command_class = request.validated['command_class']
    index = request.validated['index']
    data = get_data(request.validated['data'])
    value = network_provider.get_node_value(node_id, command_class, index)
    value.data = data
    return RestNodeValue(value)

def get_data(raw_data):
    if raw_data == 'true':
        return True
    if raw_data == 'false':
        return False
    try:
        return int(raw_data)
    except:
        return raw_data
    

class NetworkProvider(object):
    def __init__(self, my_network):
        assert isinstance(my_network, ZWaveNetwork)
        self.network = my_network
        """@type ZWaveNetwork"""

    def get_network(self):
        return self.network

    def get_nodes(self):
        return self.network.nodes

    def get_node(self, node_id):
        assert isinstance(node_id, int)
        return self.network.nodes[node_id]

    def get_node_values(self, node_id, command_class='All'):
        return [node_value
                for node_id, node_value
                in self.get_node(node_id).get_values(class_id=command_class).items()]

    def get_node_value_by_id(self, node_id, value_id):
        assert isinstance(node_id, int)
        assert isinstance(value_id, int)
        node_values = self.get_node_values(node_id)
        for node_value in node_values:
            if node_value.value_id == value_id:
                return node_value

    def get_node_value(self, node_id, command_class, index):
        assert isinstance(node_id, int)
        assert isinstance(index, int)
        node_values = self.get_node_values(node_id)
        for node_value in node_values:
            if node_value.index == index \
                    and node_value.command_class == command_class:
                return node_value


@resource(path='/network/')
class NetworkResource(object):
    def __init__(self, request):
        self.request = request
        assert isinstance(request.network, ZWaveNetwork)
        self.network_provider = NetworkProvider(request.network)
        """@type NetworkProvider"""

    @view(renderer='json')
    def get(self):
        return RestNetwork(self.network_provider.get_network())


@resource(collection_path='/nodes/', path='/node/{node_id}/')
class NodeResource(object):
    def __init__(self, request):
        self.request = request
        assert isinstance(request.network, ZWaveNetwork)
        self.network_provider = NetworkProvider(request.network)
        """@type NetworkProvider"""

    @view(renderer='json')
    def collection_get(self):
        return [RestNode(node)
                for node_id, node
                in self.network_provider.get_nodes().items()]

    @view(renderer='json')
    def get(self):
        node_id = int(self.request.matchdict['node_id'])
        return RestNode(self.network_provider.get_node(node_id))


#@resource(collection_path='/node/{node_id}/values/', path='/node/{node_id}/value/{value_id}/')
class NodeValueResource(object):
    def __init__(self, request):
        self.request = request
        assert isinstance(request.network, ZWaveNetwork)
        self.network_provider = NetworkProvider(request.network)
        """@type NetworkProvider"""

    @view(renderer='json')
    def collection_get(self):
        node_id = int(self.request.matchdict['node_id'])
        node_values = self.network_provider.get_node_values(node_id)
        return [RestNodeValue(node_value) for node_value in node_values]

    @view(renderer='json')
    def get(self):
        node_id = int(self.request.matchdict['node_id'])
        index = int(self.request.matchdict['value_d'])
        return RestNodeValue(self.network_provider.get_node_value_by_id(node_id, index))

    @view(renderer='json')
    def put(self):
        node_id = int(self.request.matchdict['node_id'])
        index = int(self.request.matchdict['value_id'])
        node_value = self.network_provider.get_node_value_by_id(node_id, index)


@resource(collection_path='/node/{node_id}/command_class/{command_class}/values/',
          path='/node/{node_id}/command_class/{command_class}/value/{index}/')
class NodeCommandClassValueResource(object):
    def __init__(self, request):
        self.request = request
        assert isinstance(request.network, ZWaveNetwork)
        self.network_provider = NetworkProvider(request.network)
        """@type NetworkProvider"""

    @view(renderer='json')
    def collection_get(self):
        node_id = int(self.request.matchdict['node_id'])
        command_class = int(self.request.matchdict['command_class'])
        node_values = self.network_provider.get_node_values(node_id, command_class)
        return [RestNodeValue(node_value) for node_value in node_values]

    @view(renderer='json')
    def get(self):
        node_id = int(self.request.matchdict['node_id'])
        command_class = int(self.request.matchdict['command_class'])
        index = int(self.request.matchdict['index'])
        return RestNodeValue(self.network_provider.get_node_value(node_id, command_class, index))
