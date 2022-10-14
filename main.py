import usocket
import _thread
import ujson
import time
import pycom
import machine
from network import WLAN
# from boards import PySense
# from lib.pycoproc_1 import Pycoproc # Para pysensev1
# from pycoproc_2 import Pycoproc #Para pysensev2

from boards.pysense1 import py_sense_api
CIAN = 0x007f7f

wlan = WLAN(mode=WLAN.STA)
wlan.antenna(WLAN.EXT_ANT)
# wlan.connect('LCD-IoT', auth=(WLAN.WPA2, '107_1AbCd'))
wlan.connect('asdasd', auth=(WLAN.WPA2, '1cdunc0rd0ba'), timeout=100)
# TimeoutError: Connection to AP Timeout!
# wlan.connect('FCEFyN', auth=(None))
print('Network found!')
while not wlan.isconnected():
    machine.idle()
print('WLAN connection succeeded!')
# wlan.ifconfig(config=('192.168.1.61', '255.255.255.0', '192.168.1.1', '192.168.1.1'))
# wlan.ifconfig(config=('172.18.119.248', '255.255.248.0', '172.18.112.1', '200.16.16.1')) # FP-18
print(wlan.ifconfig())
pycom.rgbled(CIAN)

# Set up server socket
serversocket = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
serversocket.setsockopt(usocket.SOL_SOCKET, usocket.SO_REUSEADDR, 1)
serversocket.bind(("192.168.1.101", 8000))
# serversocket.bind(("172.18.119.248", 8000)) # FP-18

# Accept maximum of 40 connections at the same time
serversocket.listen(40)

# Unique data to send back
c = 1
while True:
    # Accept the connection of the clients
    (clientsocket, address) = serversocket.accept()
    # Start a new thread to handle the client
    _thread.start_new_thread(py_sense_api.get_client_thread(), (clientsocket, c))
    c = c+1


