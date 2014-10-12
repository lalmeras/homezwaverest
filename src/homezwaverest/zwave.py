from openzwave.node import ZWaveNode
from openzwave.value import ZWaveValue
from openzwave.scene import ZWaveScene
from openzwave.controller import ZWaveController
from openzwave.network import ZWaveNetwork
from openzwave.option import ZWaveOption
import threading
import time
import sys

device="/dev/ttyACM0"

zwave_config = os.getenv('HOMEZWAVEREST_OPENZWAVE_CONFIG_PATH', '/tmp')

options = ZWaveOption(device, \
  config_path=zwave_config, \
  user_path=".", cmd_line="")
options.set_log_file("OZW_Log.log")
options.set_append_log_file(False)
options.set_console_output(False)
options.set_save_log_level('Debug')
options.set_logging(True)
options.lock()

network = ZWaveNetwork(options, log=None)

class ZWaveThread(threading.Thread):
    def run(self):
        time_started = 0
        for i in range(0,300):
            if network.state>=network.STATE_AWAKED:
        
                print(" done")
                print("Memory use : %s Mo" % (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0))
                break
            else:
                sys.stdout.write(".")
                sys.stdout.flush()
                time_started += 1
                time.sleep(1.0)
        
