from SI7006A20 import SI7006A20
from LIS2HH12 import LIS2HH12
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE

class Sensors:
    sensors = {}
    def __init__(self, pysense):
        self.sensors["light"]=LTR329ALS01(pysense)
        self.sensors["humidity"]=SI7006A20(pysense)
        self.sensors["temperature"]=SI7006A20(pysense)
        self.sensors["pressure"]=MPL3115A2(pysense, mode=PRESSURE)
        self.sensors["acceleration"]=LIS2HH12(pysense)
    
    def get_data(self, sensor):
        a = getattr(self.sensors[sensor], sensor)
        return a()
        

    def __del__(self):
        print("Object deleted")
