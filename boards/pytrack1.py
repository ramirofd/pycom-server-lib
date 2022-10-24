import ujson
import pycom
import time

from server import REST
from server import RestApi
from server import JsonResponse200
from L76GNSS import L76GNSS
from LIS2HH12 import LIS2HH12

NO_COLOUR = 0x000000

class PyTrack(RestApi):

    def __init__(self):
        super(PyTrack, self).__init__()
        self.sensors = None
        
    
    def get_data(self, sensor):
        if self.sensors is None:
            raise Exception("Pycoproc not specified. Probably forgot to call set_pycoproc method.")

        a = getattr(self.sensors[sensor], sensor)
        return a()

    def set_pycoproc(self, pycoproc):
        self.sensors = {
            "coordinates": L76GNSS(pycoproc, timeout=30),
            "acceleration": LIS2HH12(pycoproc)
        }

py_track_api = PyTrack()

@py_track_api.rest.get('/coordinates', 'Returns coordinates value')
def get_coordinates(json: str):
    resp = str(JsonResponse200(ujson.dumps({"value": py_track_api.get_data("coordinates")})))
    return resp

@py_track_api.rest.get('/acceleration', 'Returns acceleration value')
def get_acceleration(json: str):
    resp = str(JsonResponse200(ujson.dumps({"value": py_track_api.get_data("acceleration")})))
    return resp

@py_track_api.rest.post('/color', 'Change color led on the board', {'color': 'str - hexadecimal value of the RGB color'})
def post_change_color(json: str):
    d = ujson.loads(json)["color"]
    pycom.rgbled(int((d)))
    time.sleep(5)
    pycom.rgbled(NO_COLOUR)
    resp = str(JsonResponse200(ujson.dumps({"value": "OK"})))
    return resp