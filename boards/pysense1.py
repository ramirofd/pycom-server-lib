import ujson

from server import REST
from server import RestApi
from server import JsonResponse200
from lib.SI7006A20 import SI7006A20
from lib.LIS2HH12 import LIS2HH12
from lib.LTR329ALS01 import LTR329ALS01
from lib.MPL3115A2 import MPL3115A2, ALTITUDE, PRESSURE


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
def get_temperature(json: str):
    resp = str(JsonResponse200(ujson.dumps({"value": py_sense_api.get_data("humidity")})))
    return resp


@py_sense_api.rest.get('/temperature', 'Returns temperature value')
def get_temperature(json: str):
    resp = str(JsonResponse200(ujson.dumps({"value": py_sense_api.get_data("temperature")})))
    return resp


@py_sense_api.rest.get('/pressure', 'Returns pressure value')
def get_temperature(json: str):
    resp = str(JsonResponse200(ujson.dumps({"value": py_sense_api.get_data("pressure")})))
    return resp


@py_sense_api.rest.get('/acceleration', 'Returns acceleration value')
def get_temperature(json: str):
    resp = str(JsonResponse200(ujson.dumps({"value": py_sense_api.get_data("acceleration")})))
    return resp

@py_sense_api.rest.post('/led_color', 'Changes the color of the LED', {'color':'int - The hexadecimal value of the color to be set.'})
def post_led_color(json: str):
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
    return resp