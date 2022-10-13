from server import Server
from server import JsonResponse200
import ujson
from boards import Sensors
from pycoproc_1 import Pycoproc # Para pysensev1
# from pycoproc_2 import Pycoproc #Para pysensev2

# Para pysensev2
# py = Pycoproc()
# if py.read_product_id() != Pycoproc.USB_PID_PYSENSE:
#     raise Exception('Not a Pysense')
# Fin para pysensev2
py = Pycoproc(Pycoproc.PYSENSE) #Para pysensev1
pySensor = Sensors(py)
server = Server()


@server.get('/temperature')
def get_temperature(json: str):
    return str(JsonResponse200(ujson.dumps({"value": pySensor.get_data("temperature")})))

print(type(get_temperature("temperature").encode()))


