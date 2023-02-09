from time import time
import ujson
import pycom
import time

from server import REST
from server import RestApi
from server import JsonResponse200
from SI7006A20 import SI7006A20
from LIS2HH12 import LIS2HH12
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2, PRESSURE

NO_COLOUR = 0x000000

class PySense(RestApi):

    def __init__(self):
        super(PySense, self).__init__()
        self.sensors = None
        
    
    def get_data(self, sensor):
        if self.sensors is None:
            raise Exception("Pycoproc not specified. Probably forgot to call set_pycoproc method.")

        a = getattr(self.sensors[sensor], sensor)
        return a()

    def set_pycoproc(self, pycoproc):
        light_lux = LTR329ALS01(pycoproc)
        accelero = LIS2HH12(pycoproc)
        self.sensors = {
            "light": light_lux,
            "lux": light_lux,
            "humidity": SI7006A20(pycoproc),
            "temperature": SI7006A20(pycoproc),
            "pressure": MPL3115A2(pycoproc, mode=PRESSURE),
            "acceleration": accelero,
            "roll": accelero,
            "pitch": accelero
        }

py_sense_api = PySense()

@py_sense_api.rest.get('/light', 'Returns light value of the light sensor')
def get_temperature(json: str):
    resp = str(JsonResponse200(ujson.dumps({"value": py_sense_api.get_data("light")})))
    return resp

@py_sense_api.rest.get('/humidity', 'Returns humidity value')
def get_humidity(json: str):
    resp = str(JsonResponse200(ujson.dumps({"value": py_sense_api.get_data("humidity")})))
    return resp

@py_sense_api.rest.get('/temperature', 'Returns temperature value')
def get_temperature(json: str):
    resp = str(JsonResponse200(ujson.dumps({"value": py_sense_api.get_data("temperature")})))
    return resp

@py_sense_api.rest.get('/pressure', 'Returns pressure value')
def get_pressure(json: str):
    resp = str(JsonResponse200(ujson.dumps({"value": py_sense_api.get_data("pressure")})))
    return resp

@py_sense_api.rest.get('/acceleration', 'Returns acceleration value')
def get_acceleration(json: str):
    resp = str(JsonResponse200(ujson.dumps({"value": py_sense_api.get_data("acceleration")})))
    return resp

@py_sense_api.rest.get('/lux', 'Returns the illuminance value of the light sensor')
def get_temperature(json: str):
    resp = str(JsonResponse200(ujson.dumps({"value": py_sense_api.get_data("lux")})))
    return resp

@py_sense_api.rest.get('/roll', 'Returns the roll value of the accelerometer')
def get_temperature(json: str):
    resp = str(JsonResponse200(ujson.dumps({"value": py_sense_api.get_data("roll")})))
    return resp

@py_sense_api.rest.get('/pitch', 'Returns the pitchj value of the accelerometer')
def get_temperature(json: str):
    resp = str(JsonResponse200(ujson.dumps({"value": py_sense_api.get_data("pitch")})))

@py_sense_api.rest.post('/color', 'Change color led on the board', {
    'color': 'str - hexadecimal value of the RGB color',
    'duration': 'int - duration in seconds to keep led on before turning it off'
})
def post_change_color(json: str):
    color = ujson.loads(json).get("color", None)
    duration = ujson.loads(json).get("duration", None) 
    if color is None:
        resp = str(JsonResponse400(ujson.dumps({"value": "Failed because you forgot to send the color code"})))
        return resp
    pycom.rgbled(int((color)))
    if duration is not None:
        time.sleep(duration)
        pycom.rgbled(NO_COLOUR)
    resp = str(JsonResponse200(ujson.dumps({"value": "OK"})))
    return resp