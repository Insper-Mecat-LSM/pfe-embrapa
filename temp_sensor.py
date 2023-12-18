from onewire import DS18X20
from onewire import OneWire
from machine import Pin
import time

class TempSensor:
  def __init__(self, pinNumber):
    self.oneWire = OneWire(Pin(pinNumber))
    self.temp = DS18X20(self.oneWire)
  
  def start_measure(self):
    self.temp.start_conversion()
    time.sleep(1)
    #print(self.temp.read_temp_async())
    #time.sleep(1)
    return self.temp.read_temp_async()