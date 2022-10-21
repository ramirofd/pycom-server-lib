import usocket
import machine
from network import WLAN
from network import MDNS
import _thread

from .api import RestApi


class Network:
    def __init__(self, ssid:str, pwd:str=None, config:tuple=None):
        self.ssid = ssid
        self.pwd = pwd
        self.config = config

    def as_dict(self):
        return {
            self.ssid: {
                'pwd': self.pwd,
                'wlan_config': self.config
            }
        }
    

class WlanServer:
    def __init__(self, ext_ant:bool=True, api:RestApi=None, port:int=8000, 
                ap_mode_ssid:str='Pycom-Node', ap_mode_auth:tuple=None, 
                ap_mode_channel:int=6, service_name:str='pycom_edu_api'):
        self.wlan = WLAN(mode=WLAN.STA)

        if ext_ant:
            self.wlan.antenna(WLAN.EXT_ANT)
            self.ap_mode_antenna = WLAN.EXT_ANT 
        else:
            self.wlan.antenna(WLAN.INT_ANT)
            self.ap_mode_antenna = WLAN.INT_ANT 
        
        if api is None:
            raise Exception("API not specified. Need an API to start server!")
        else:
            self.api = api
        self.port = port

        self.ap_mode_ssid = ap_mode_ssid
        self.ap_mode_auth = ap_mode_auth
        self.ap_mode_channel = ap_mode_channel

        self.service_name = service_name

    """
    nets: shoud be a list of Networks
    ToDo
    """
    def connect(self, nets:list=None):
        known_nets = dict()
        for net in nets:
            known_nets.update(net.as_dict())
        print("Scanning for known wifi nets")
        available_nets = self.wlan.scan()
        available_nets_names = frozenset([e.ssid for e in available_nets])
        known_nets_names = frozenset([key for key in known_nets])
        net_to_use = list(available_nets_names & known_nets_names)
        net_index = 0
        connected = False
        while not connected and net_index<len(net_to_use):
            current_network = net_to_use[net_index]
            try:
                print('Trying to connect to: {network}'.format(network=current_network))
                net_properties = known_nets[current_network]
                pwd = net_properties['pwd']
                sec = [e.sec for e in available_nets if e.ssid == current_network][0]
                wlan_config = net_properties.get('wlan_config', None)
                if wlan_config is not None:
                    self.wlan.ifconfig(config=wlan_config)

                if pwd is None:
                    self.wlan.connect(current_network, auth=None, timeout=10000)
                else:
                    self.wlan.connect(current_network, auth=(sec, pwd), timeout=10000)
                
                while not self.wlan.isconnected():
                    machine.idle() # save power while waiting
                print('Success connecting to: {network}'.format(network=current_network))
                connected = True

            except Exception as err:
                print('Failed connecting to: {network}'.format(network=current_network))
                net_index += 1 
                print('Trying the next available network')

        if connected:
            self.on_connect_success()
        else:
            print("Failed to connect to any known network, going into AP mode")
            self.wlan.init(mode=WLAN.AP, ssid=self.ap_mode_ssid, auth=self.ap_mode_auth, channel=self.ap_mode_channel, antenna=self.ap_mode_antenna)
            self.on_connect_success()



    def on_connect_success(self):
        # Set up server socket
        serversocket = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
        serversocket.setsockopt(usocket.SOL_SOCKET, usocket.SO_REUSEADDR, 1)
        serversocket.bind((self.wlan.ifconfig()[0], self.port))

        # Accept maximum of 40 connections at the same time
        serversocket.listen(40)
        print('Server started on: {ip}:{port}'.format(ip=self.wlan.ifconfig()[0], port=self.port))

        # Start MDNS 
        MDNS.init()
        MDNS.set_name(hostname = self.ap_mode_ssid)
        MDNS.add_service("_{service}".format(service=self.service_name), MDNS.PROTO_TCP, 8000)
        # Unique data to send back
        c = 1
        while True:
            # Accept the connection of the clients
            (clientsocket, address) = serversocket.accept()
            # Start a new thread to handle the client
            _thread.start_new_thread(self.api.get_client_thread(), (clientsocket, c))
            c = c+1