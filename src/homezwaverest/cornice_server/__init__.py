"""Main entry point
"""
from ConfigParser import ConfigParser
from homezwaverest.zwave import load_network
from pyramid.config import Configurator


class NetworkProvider(object):
    def __init__(self, network):
        self.network = network

    def __call__(self, request):
        """
        :rtype ZWaveNetwork
        """
        return self.network

def main(global_config, **settings):
    parser = ConfigParser()
    if not global_config.has_key('homezwaverest.configuration'):
        raise KeyError('homezwaverest.configuration must be set')
    else:
        try:
            parser.read(global_config['homezwaverest.configuration'])
        except Exception, e:
            raise IOError('Error reading configuration file %s' % (global_config['homezwaverest.configuration'], ))
    config = Configurator(settings=settings)
    for section in parser.sections():
        hsettings = dict()
        hsettings[section] = dict(parser.items(section))
        config.add_settings(hsettings)

    hsettings = config.get_settings()['homezwaverest']
    network = load_network(hsettings['openzwave.device'],
                           hsettings['openzwave.configuration_path'],
                           hsettings['openzwave.user_path'],
                           'OZW.log')

    config.set_request_property(NetworkProvider(network), name='network')
    config.include("cornice")
    config.include("homezwaverest.cornice_server.views")
    config.scan("homezwaverest.cornice_server.views")
    return config.make_wsgi_app()
