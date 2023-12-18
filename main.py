from machine import Pin, ADC, UART, deepsleep
import esp32
from temp_sensor import TempSensor
from ph_sensor import PhSensor
from gps import GPS
from I2C import *
import urandom
import json
import time
import requests

I2C_ADDR = 0x27
totalRows = 4
totalColumns = 20

sdaPIN = 21
sclPIN = 22

display_lcd = I2C_Display(I2C_ADDR, totalRows, totalColumns, sdaPIN, sclPIN)

keys = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'

def randstr(length=10, aSeq=keys):
    return ''.join((urandom.choice(aSeq) for _ in range(length)))



# Tenta ler o arquivo
nome_arquivo="gps.txt"
flag_vazio = False
try:
    with open(nome_arquivo, 'r') as arquivo:
        conteudo = arquivo.read()
        if not conteudo:
            flag_vazio = True
        else:
            flag_vazio = False
            # Se o arquivo não estiver vazio, armazena os dois valores lidos em duas variáveis
            linhas = conteudo.split('\n')
            if len(linhas) >= 2:
                latitude = linhas[0]
                longitude = linhas[1]
                identifier = linhas[2]
            else:
                print("O arquivo não contém pelo menos dois valores.")
except Exception as e:
    # Se o arquivo não existir, cria-o na raiz do projeto
    with open(nome_arquivo, 'w') as novo_arquivo:
        flag_vazio = True
        
        print(f"O arquivo {nome_arquivo} não foi encontrado e foi criado na raiz do projeto.")



if flag_vazio:
    gpsSensor = GPS()
    gpsSensor.test_connection()
    latitude, longitude = gpsSensor.try_get_location()
    identifier = randstr()
    with open(nome_arquivo, 'w') as arquivo_gps:
        arquivo_gps.write(f"{latitude}\n{longitude}\n{identifier}")

        print("Dados de latitude e longitude foram escritos no arquivo.")

batery_level = ADC(Pin(36))
batery_level.atten(ADC.ATTN_11DB)

# configs ph_sensor
phSensorPin = ADC(Pin(34))
phSensorPin.atten(ADC.ATTN_11DB)
samples_ph_sensor = 10

phSensor = PhSensor(phSensorPin, samples_ph_sensor)

# configs temp_sensor
temperature_sensor_short = TempSensor(32)
temperature_sensor_long = TempSensor(33)

user_wifi='4G-UFI-F008'
password_wifi='1234567890'

def do_connect(user_wifi, password_wifi):
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(user_wifi, password_wifi)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
    
do_connect(user_wifi, password_wifi)
    
url = "https://jxqq6yoosk.execute-api.us-east-2.amazonaws.com"

def read_task():
    
    sensor_data = read_sensors()

    # Fazer uma solicitação POST para o endpoint
    response = requests.post(url, json=sensor_data)

    # Verificar a resposta
    if response.status_code == 200:
        print("POST dados do sensor enviado!")
        json_string = response.text
        
        # Primeiro, carregue a string JSON em um dicionário Python
        #data = json.loads(json_string)
        print(json_string)

        
    else:
        print("Erro no POST. Código de status:", response.status_code)

def read_sensors():    
    #o2_dissolved = round(random.uniform(0, 100), 2)
    temperature_short = temperature_sensor_short.start_measure()
    temperature_long = temperature_sensor_long.start_measure()
    
    if temperature_long and temperature_short:
        dicionario = {}
        dicionario["latitude"] = latitude
        dicionario["longitude"] = longitude
        dicionario["identifier"] = identifier
        dicionario["temperature_short"] = temperature_short
        dicionario["temperature_long"] = temperature_long
        dicionario["ph"] = phSensor.start_measure()
        return dicionario
        #return json.loads({
        #    "latitude": latitude,
        #    "longitude": longitude,
        #    "identifier": identifier,
        #    "temperature_short": temperature_short,
        #    "temperature_long": temperature_long,
        #    "ph": phSensor.start_measure(),
        #    #"o2_dissolved": o2_dissolved,
        #})
    else:
        return False

while True:
    print(ligar_display)
    display_lcd.turnoff_lcd()
    if ligar_display == True:
        display_lcd.turnon_lcd()
    data = read_sensors()
    print(data)
    if(data != False):
        temperature_short = str(round(data["temperature_short"],2))
        temperature_long = str(round(data["temperature_long"], 2))
        ph = str(round(data["ph"],1))
        read_task()
        bateria = round((100 * int(batery_level.read()))/4096, 2)
        display_lcd.write_data(temperature_short, temperature_long, ph, bateria)
        time.sleep(10)
        display_lcd.turnoff_lcd()
    print("Indo dormir ZZZZZZZ.....")
    deepsleep(2000) #2 segundos

