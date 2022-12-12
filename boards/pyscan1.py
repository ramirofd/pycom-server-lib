from time import time
import ujson
import pycom
import time

from server import REST
from server import RestApi
from server import JsonResponse200
from LIS2HH12 import LIS2HH12
from LTR329ALS01 import LTR329ALS01
from MFRC630 import MFRC630

NO_COLOUR = 0x000000

ID = 0
ID1 = []
CARDkey = [ 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF ]
DECODE_CARD = False

counter = 0

class PyScan(RestApi):

    def __init__(self):
        super(PyScan, self).__init__()
        self.sensors = None
        self.lector = None
        self.counter = 0
        self.py = None
    
    def get_data(self, sensor):
        if self.sensors is None:
            raise Exception("Pycoproc not specified. Probably forgot to call set_pycoproc method.")

        a = getattr(self.sensors[sensor], sensor)
        return a()

    def set_pycoproc(self, pycoproc):
        self.sensors = {
            "light": LTR329ALS01(pycoproc),
            "acceleration": LIS2HH12(pycoproc)
        }
        self.py = pycoproc

    def read(self):
        global ID, counter
        nfc = MFRC630(self.py)
        nfc.mfrc630_cmd_init()
        while(True):
            atqa = nfc.mfrc630_iso14443a_WUPA_REQA(nfc.MFRC630_ISO14443_CMD_REQA)
            if (atqa != 0):
                uid = bytearray(10)
                uid_len = nfc.mfrc630_iso14443a_select(uid)
                if (uid_len > 0):
                    counter += 1
                    ID = nfc.format_block(uid, uid_len)
                    print(ID)
                    if(len(ID1) == 10):
                        ID1.pop(0)
                    ID1.append(ID)
                    break
        return ID
    
    def reader(self):
        if(len(ID1) == 10):
            print("Hola")
        return ID1

py_scan_api = PyScan()

@py_scan_api.rest.get('/light', 'Returns light value')
def get_light(json: str):
    resp = str(JsonResponse200(ujson.dumps({"value": py_scan_api.get_data("light")})))
    return resp

@py_scan_api.rest.get('/acceleration', 'Returns acceleration value')
def get_acceleration(json: str):
    resp = str(JsonResponse200(ujson.dumps({"value": py_scan_api.get_data("acceleration")})))
    return resp

@py_scan_api.rest.get('/id', 'Return ID card read')
def card_id(json: str):
    resp = str(JsonResponse200(ujson.dumps({"value": py_scan_api.read()})))
    return resp

@py_scan_api.rest.get('/lastid', 'Return the last ID card read')
def card_id(json: str):
    resp = str(JsonResponse200(ujson.dumps({"value": py_scan_api.reader()})))
    return resp

@py_scan_api.rest.post('/color', 'Change color led on the board', {'color': 'str - hexadecimal value of the RGB color'})
def post_change_color(json: str):
    d = ujson.loads(json)["color"]
    pycom.rgbled(int((d)))
    time.sleep(5)
    pycom.rgbled(NO_COLOUR)
    resp = str(JsonResponse200(ujson.dumps({"value": "OK"})))
    return resp
