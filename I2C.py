from machine import Pin, SoftI2C
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
import machine
from time import sleep

class I2C_Display:
    def __init__(self, I2C_ADDR, totalRows, totalColumns, sdaPIN, sclPIN):
        self.I2C_ADDR = I2C_ADDR
        self.totalRows = totalRows
        self.totalColumns = totalColumns
        self.sdaPIN = sdaPIN
        self.sclPIN = sclPIN
        self.i2c = machine.I2C(sda=self.sdaPIN, scl=self.sclPIN, freq=10000)
        self.i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=10000)
        self.lcd = I2cLcd(self.i2c, self.I2C_ADDR, self.totalRows, self.totalColumns)
        self.devices = self.i2c.scan()
        self.address = ""
    
    def scan_devices(self):
        while True:
            if len(self.devices) == 0:
                print("No i2c device !")
            else:
                print('i2c devices found:',len(self.devices))
             
            for device in self.devices:
             
                print("At address: ",hex(device))
                self.address = hex(device)
                break
        
    def write_data(self, temperature_short, temperature_long, ph, battery):
        self.lcd.clear()
        self.lcd.move_to(0,0)
        self.lcd.putstr(f"Temp curta: {temperature_short}\n")
        self.lcd.move_to(0,1)
        self.lcd.putstr(f"Temp longa: {temperature_long}\n")
        self.lcd.move_to(0,2)
        self.lcd.putstr(f"Ph: {ph}\n")
        self.lcd.move_to(0,3)
        self.lcd.putstr(f"Bateria: {battery}\n")
        sleep(1)
        
    def turnoff_lcd(self):
        self.lcd.display_off()
        self.lcd.backlight_off()
    
    def turnon_lcd(self):
        self.lcd.display_on()
        self.lcd.backlight_on()
        
        
        