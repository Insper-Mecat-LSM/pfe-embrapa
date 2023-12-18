import re
import machine
import time
from machine import UART

# Configurar a porta serial (ajuste os pinos RX e TX de acordo com o seu hardware)
uart = UART(1, baudrate=115200, tx=27, rx=26)  # UART1

# Seu código para configuração do UART
def send_at_command(command):
    uart.write(command + '\r\n')
    time.sleep(1)  # Aguarde um momento para a resposta
    response = ""
    
    while uart.any():
        response += uart.read(1).decode('utf-8')
    
    return response

while True:
    at_command = input("Digite o comando AT (ou 'exit' para sair): ")
    if at_command == 'exit':
        break
    response = send_at_command(at_command)
    print("Resposta do dispositivo:", response)
    
    #print(response.split(","))
    #LATITUDE = response.split(",")[3]
    #LONGITUDE = response.split(",")[4]
    #print(LATITUDE, LONGITUDE)
    
    

