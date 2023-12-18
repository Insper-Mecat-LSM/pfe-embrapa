# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

import time
from machine import Pin
import esp32

wake1 = Pin(4, mode = Pin.IN)
esp32.wake_on_ext0(pin = wake1, level = esp32.WAKEUP_ANY_HIGH)

ligar_display = False

if wake1.value() == 1:
    ligar_display = True
print(ligar_display)

print("Start GPS")
Pin(4, Pin.OUT).on()
time.sleep(4)

print("GPS Inicializado")