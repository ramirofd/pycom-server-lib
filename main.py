from lib.pycoproc_1 import Pycoproc
# from boards.pysense1 import py_sense_api
# from boards.pytrack1 import py_track_api
from boards.pyscan1 import py_scan_api
from server import WlanServer
from server import Network

import pycom

pycom.heartbeat(False)

# py = Pycoproc(Pycoproc.PYSENSE)
# py = Pycoproc(Pycoproc.PYTRACK)
py = Pycoproc(Pycoproc.PYSCAN)
# py_sense_api.set_pycoproc(py)
# py_track_api.set_pycoproc(py)
py_scan_api.set_pycoproc(py)

# server = WlanServer(api=py_sense_api)
# server = WlanServer(api=py_track_api)
server = WlanServer(api=py_scan_api)
nets = [
    Network(ssid='LCD', pwd='1cdunc0rd0ba'),
    Network(ssid='NoTengoWiFi', pwd='nohaywifi'),
    Network(ssid='FCEFyN')
]

while True:
    py_scan_api.get_card_id(py_scan_api.lector,py_scan_api.counter)
    # server.connect(nets=nets)

