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

class PyScan(RestApi):

    def __init__(self):
        super(PyScan, self).__init__()
        self.sensors = None
        self.lector = None
        self.counter = 0
    
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
        self.lector = MFRC630(pycoproc)

    def get_card_id(self,lector,counter):
        lector.mfrc630_cmd_init()
        atqa = lector.mfrc630_iso14443a_WUPA_REQA(lector.MFRC630_ISO14443_CMD_REQA)
        if(atqa!= 0):
            print("A card has been detected, reading its UID ...")
            uid = bytearray(10)
            uid_len= lector.mfrc630_iso14443a_select(uid)
            print('\tUID has length: {}'.format(uid_len))
            if(uid_len > 0):
                counter += 1
                print("\tUID [{}]: {}".format(uid_len, lector.format_block(uid, uid_len)))

        lector.mfrc630_cmd_reset()
        time.sleep(.5)
        lector.mfrc630_cmd_init()

py_scan_api = PyScan()

@py_scan_api.rest.get('/light', 'Returns light value')
def get_light(json: str):
    resp = str(JsonResponse200(ujson.dumps({"value": py_scan_api.get_data("light")})))
    return resp

@py_scan_api.rest.get('/acceleration', 'Returns acceleration value')
def get_acceleration(json: str):
    resp = str(JsonResponse200(ujson.dumps({"value": py_scan_api.get_data("acceleration")})))
    return resp

@py_scan_api.rest.post('/color', 'Change color led on the board', {'color': 'str - hexadecimal value of the RGB color'})
def post_change_color(json: str):
    d = ujson.loads(json)["color"]
    pycom.rgbled(int((d)))
    time.sleep(5)
    pycom.rgbled(NO_COLOUR)
    resp = str(JsonResponse200(ujson.dumps({"value": "OK"})))
    return resp

def card_id():
    print("Holaaaaa")
    return py_scan_api.get_card_id(py_scan_api.lector)