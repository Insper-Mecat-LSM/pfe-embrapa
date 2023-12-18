import machine
import time
from machine import UART, Pin

# Configurar a porta serial (ajuste os pinos RX e TX de acordo com o seu hardware)
uart = UART(1, baudrate=115200, tx=27, rx=26)  # UART1

def send_at_command(command):
    
    uart.write(command + '\r\n')
    time.sleep(1)  # Aguarde um momento para a resposta
    response = ""
    while uart.any():
        response += uart.read(1).decode('utf-8')
        
    return response

time.sleep(1)
response = send_at_command("AT")
print("Resposta do dispositivo:", response)

time.sleep(1)
response = send_at_command("AT")
print("Resposta do dispositivo:", response)

time.sleep(1)
response = send_at_command("AT+CGNSPWR=1")
print("Resposta do dispositivo:", response)

time.sleep(1)
response = send_at_command("AT+SGPIO=0,4,1,1")
print("Resposta do dispositivo:", response)


while True:
    
    
    at_command = input("Digite o comando AT (ou 'exit' para sair): ")
    if at_command == 'exit':
        break
    response = send_at_command(at_command)
    print("Resposta do dispositivo:", response)


