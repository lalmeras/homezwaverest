import atexit
from time import sleep
import threading
import time
import sys
import os
import signal
import logging

from openzwave.node import ZWaveNode
from openzwave.value import ZWaveValue
from openzwave.scene import ZWaveScene
from openzwave.controller import ZWaveController
from openzwave.network import ZWaveNetwork
from openzwave.option import ZWaveOption


log = logging.getLogger(__name__)
_NETWORKS = []


def load_network(device, openzwave_config_path, openzwave_user_path, log_file):
    """
    :param device: /dev/ttyXXX device controller
    :param openzwave_config_path: path where openzwave xml configuration files are stored
    :param openzwave_user_path: path where openzwave user configuration files are stored
    :return: a zave network
    :rtype ZWaveNetwork
    """
    options = ZWaveOption(device, config_path=openzwave_config_path, user_path=openzwave_user_path, cmd_line='')
    options.set_log_file(log_file)
    options.set_append_log_file(False)
    options.set_console_output(False)
    options.set_save_log_level('Debug')
    options.set_logging(True)
    options.lock()

    network = ZWaveNetwork(options, log=None)
    _NETWORKS.append(network)
    return network


def openzwave_stop():
    log.info('Shutdown asked - notifying networks...')
    for network in _NETWORKS:
        network.stop()
    log.info('openzwave stopped.')


log.info('Registering SIGTERM handler.')
atexit.register(openzwave_stop)


def raise_system_exit(signum, frame):
    raise SystemExit


signal.signal(signal.SIGTERM, raise_system_exit)