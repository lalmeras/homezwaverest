"""Main entry point
"""
from pyramid.config import Configurator


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include("cornice")
    config.include("homezwaverest.cornice_server.views")
    config.scan("homezwaverest.cornice_server.views")
    return config.make_wsgi_app()
