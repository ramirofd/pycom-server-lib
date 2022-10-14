import ujson

from server import REST
from server import RestApi
from server import JsonResponse200
from lib.SI7006A20 import SI7006A20
from lib.LIS2HH12 import LIS2HH12
from lib.LTR329ALS01 import LTR329ALS01
from lib.MPL3115A2 import MPL3115A2, ALTITUDE, PRESSURE

from lib.pycoproc_1 import Pycoproc #Para pysensev1


class PySense(RestApi):

    def __init__(self, pysense):
        super(PySense, self).__init__()
        self.sensors = {
            "light": LTR329ALS01(pysense),
            "humidity": SI7006A20(pysense),
            "temperature": SI7006A20(pysense),
            "pressure": MPL3115A2(pysense, mode=PRESSURE),
            "acceleration": LIS2HH12(pysense)
        }
    
    def get_data(self, sensor):
        a = getattr(self.sensors[sensor], sensor)
        return a()

py = Pycoproc(Pycoproc.PYSENSE)
py_sense_api = PySense(py)


@py_sense_api.rest.get('/light')
def get_temperature(json: str):
    resp = str(JsonResponse200(ujson.dumps({"value": py_sense_api.get_data("light")})))
    return resp


@py_sense_api.rest.get('/humidity')
def get_temperature(json: str):
    resp = str(JsonResponse200(ujson.dumps({"value": py_sense_api.get_data("temperature")})))
    return resp


@py_sense_api.rest.get('/temperature')
def get_temperature(json: str):
    resp = str(JsonResponse200(ujson.dumps({"value": py_sense_api.get_data("temperature")})))
    return resp


@py_sense_api.rest.get('/pressure')
def get_temperature(json: str):
    resp = str(JsonResponse200(ujson.dumps({"value": py_sense_api.get_data("temperature")})))
    return resp


@py_sense_api.rest.get('/acceleration')
def get_temperature(json: str):
    resp = str(JsonResponse200(ujson.dumps({"value": py_sense_api.get_data("temperature")})))
    return resp