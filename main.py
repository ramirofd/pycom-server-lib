# from lib.pycoproc_1 import Pycoproc # Para pysensev1
from lib.pycoproc_2 import Pycoproc #Para pysensev2
from boards.pysense1 import py_sense_api
from server import WlanServer
from server import Network

import pycom
pycom.heartbeat(False)

# py = Pycoproc(Pycoproc.PYSENSE)
py = Pycoproc()
py_sense_api.set_pycoproc(py)

server = WlanServer(api=py_sense_api)
nets = [
    Network(ssid='LCD', pwd='1cdunc0rd0ba'),
    Network(ssid='NoTengoWiFi', pwd='nohaywifi'),
    # Network(ssid='FCEFyN')
]
server.connect(nets=nets)



