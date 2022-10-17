from lib.pycoproc_1 import Pycoproc # Para pysensev1
# from lib.pycoproc_2 import Pycoproc #Para pysensev2
from boards.pysense1 import py_sense_api
from server import WlanServer
from server import Network


py = Pycoproc(Pycoproc.PYSENSE)
py_sense_api.set_pycoproc(py)

server = WlanServer(api=py_sense_api)
nets = [
    Network(ssid='NoTengoWiFi', pwd='nohaywifi'),
    Network(ssid='FCEFyN')
]
server.connect(nets=nets)



