import time
from machine import UART, Pin
import re

class GPS:
    def __init__(self):
        # Configurar a porta serial (ajuste os pinos RX e TX de acordo com o seu hardware)
        self.uart = UART(1, baudrate=115200, tx=27, rx=26)  # UART1
    
    def send_at_command(self, command):
    
        self.uart.write(command + '\r\n')
        time.sleep(1)  # Aguarde um momento para a resposta
        response = ""
        while self.uart.any():
            response += self.uart.read(1).decode('utf-8')
        
        return response
    
    def test_connection(self):
        time.sleep(1)
        response = self.send_at_command("AT")
        print("Resposta do dispositivo:", response)

        time.sleep(1)
        response = self.send_at_command("AT")
        print("Resposta do dispositivo:", response)

        time.sleep(1)
        response = self.send_at_command("AT+CGNSPWR=1")
        print("Resposta do dispositivo:", response)

        time.sleep(1)
        response = self.send_at_command("AT+SGPIO=0,4,1,1")
        print("Resposta do dispositivo:", response)
        
    def get_lat_long(self):
        response = ""
        while True:
            self.uart.write("AT+CGNSINF\r\n")
            time.sleep(1)  # Aguarde um momento para a resposta
            while self.uart.any():
                response += self.uart.read(1).decode('utf-8')
            print(response)
            if "+CGNSINF:" in response:
                match = re.search(r'[-+]?[0-9]*\.?[0-9]+,[-+]?[0-9]*\.?[0-9]+', response)
                if match:
                    latitude, longitude = response.split(',')[3:5]
                    
                    
                    return latitude, longitude
            response = ""  # Limpar a resposta e tentar novamente

    def try_get_location(self):
        # Loop para enviar o comando até obter a resposta desejada
        while True:
            latitude, longitude = self.get_lat_long()
            if latitude and longitude:
                print("Latitude:", latitude)
                print("Longitude:", longitude)
                
                break
            print("Buscando...")
        return latitude, longitude
