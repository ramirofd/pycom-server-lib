import pwd
import usocket
from network import WLAN
import _thread

from api import RestApi
class Network:
    def __init__(self, ssid:str, pwd:str, config:tuple):
        self.ssid = ssid
        self.pwd = pwd
        self.config = config


class WlanServer:
    def __init__(self, ext_ant:bool=True, api:RestApi=None, port:int=8000):
        self.wlan = WLAN(mode=WLAN.STA)
        if ext_ant:
            self.wlan.antenna(WLAN.EXT_ANT)
        if api is None:
            raise Exception("API not specified. Need an API to start server!")
        else:
            self.api = api

        self.port = port

    """
    nets: shoud be a list of Networks
    ToDo
    """
    def connect(self, nets:list=None):
        print("Scanning for known wifi nets")
        available_nets = self.wlan.scan()
        known_available_nets = []

    def on_connect_success(self):
        # Set up server socket
        serversocket = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
        serversocket.setsockopt(usocket.SOL_SOCKET, usocket.SO_REUSEADDR, 1)
        serversocket.bind((self.wlan.ifconfig()[0], self.port))

        # Accept maximum of 40 connections at the same time
        serversocket.listen(40)

        # Unique data to send back
        c = 1
        while True:
            # Accept the connection of the clients
            (clientsocket, address) = serversocket.accept()
            # Start a new thread to handle the client
            _thread.start_new_thread(self.api.get_client_thread(), (clientsocket, c))
            c = c+1