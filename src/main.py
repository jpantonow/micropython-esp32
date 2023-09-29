from i2c_lcd import I2cLcd
from lcd_api import LcdApi
from machine import SoftI2C, Pin, Timer, ADC
import machine
import network
import time
from umqtt.robust import MQTTClient
import sys #Utilizado para terminar o programa
import dht
#Garagem de Bike
from machine import Pin, PWM
from servo import Servo
from time import sleep

LCD_ENTRADA = 0x27 #Entrada
LCD_SOTAO = 0x26 #Sotao
totalRows = 2
totalColumns = 16
i2c = SoftI2C(scl = Pin(22), sda = Pin(21), freq = 10000)
lcd_entrada = I2cLcd(i2c,LCD_ENTRADA,totalRows,totalColumns)
lcd_sotao = I2cLcd(i2c,LCD_SOTAO,totalRows,totalColumns)


RELE1_PIN = 25 #Ar Condicionado
RELE2_PIN = 26 #Geladeira
rele1 = machine.Pin(RELE1_PIN, machine.Pin.OUT)
rele2 = machine.Pin(RELE2_PIN, machine.Pin.OUT)


# Definindo os pinos
motor = Servo(pin=13) # Pino onde o servo está conectado
button_pin = 14 # Pino onde o botão está conectado
porta = 0       #0 => Fechada; 1 => Aberta

# Configurando o botão
button = Pin(button_pin, Pin.IN, Pin.PULL_UP)

# Posição inicial do servo
motor.move(0)

# Configuração do ADC para o MQ-135 no pino GPIO 34
mq135 = ADC(Pin(34))
mq135.atten(ADC.ATTN_11DB)  # Configura a atenuação para uma faixa de 0-3.3V

# Configuração do LED interno no pino GPIO 2
led = Pin(2, Pin.OUT)

# Variáveis para calibração
calibration_time = 60  # 60 segundos para calibração
calibration_sum = 0
calibration_count = 0

# Realiza a calibração durante os primeiros 60 segundos
print("Calibrando sensor MQ-135. Por favor, aguarde...")
start_time = time()
while time() - start_time < calibration_time:
    calibration_sum += mq135.read()
    calibration_count += 1
    sleep(1)
calibration_avg = calibration_sum / calibration_count
print("Calibração concluída. Valor médio: ", calibration_avg)

# Função para calcular a concentração de CO2 (aproximada)
def calculate_ppm(adc_value, calibration_value):
    return ((float(adc_value) / calibration_value) - 0.42) * (10000 / 0.92)/10


def cb(topic,msg):
    if topic == b"jpgomes/feeds/ar_condicionado":
        if msg ==b"0":
            rele1.value(0)
        if msg == b"1": 
            rele1.value(1)
    if topic == b"jpgomes/feeds/geladeira":
        if msg == b"0":
            rele2.value(0)
        if msg == b"1":
            rele2.value(1)
    if topic == b"jpgomes/feeds/led_entrada":
        if msg == b"0":
            lcd_entrada.clear()
        if msg == b"1":
            lcd_entrada.putstr("Bem vindo!")
            time.sleep(2)
    if topic == b"jpgomes/feeds/led_sotao":
        if msg == b"0":
            lcd_sotao.clear()
        if msg == b"1":
            lcd_sotao.putstr("Hoje está quente!")
            time.sleep(2)
    if topic == b"jpgomes/feeds/motor":
        if msg == b"0":
            #if porta == 0:
            motor.move(90)
            sleep(1)
            porta = 1
        if msg == b"1":
            #if porta == 1:
            motor.move(0)
            sleep(1)
            porta = 0


sensor = dht.DHT11(Pin(15))                  # DHT11 Sensor on Pin 4 of ESP32

led=Pin(2,Pin.OUT)                          # Onboard LED on Pin 2 of ESP32

WIFI_SSID     = 'Wokwi-GUEST'
WIFI_PASSWORD = ''

mqtt_client_id      = bytes('client_'+'12321', 'utf-8') # Just a random client ID

ADAFRUIT_IO_URL     = 'io.adafruit.com' 
ADAFRUIT_USERNAME   = 'jpgomes'
ADAFRUIT_IO_KEY     = 'aio_vuMx53el1tc7X4IlJTuNxbhPdUxZ'

# ============= FEEDs ============= #
TOGGLE_FEED_ID_1      = 'ar_condicionado'
TOGGLE_FEED_ID_2      = 'geladeira'
TOGGLE_FEED_ID_3 = 'motor'
TOGGLE_FEED_ID_4 = 'led_entrada'
TOGGLE_FEED_ID_5 = 'led_sotao'
TEMP_FEED_ID      = 'temp'
HUM_FEED_ID      = 'hum'

def connect_wifi(): #Função para conectar no WIFI
  print("Connecting to WiFi", end="")
  sta_if = network.WLAN(network.STA_IF)
  sta_if.active(True)
  sta_if.connect(WIFI_SSID, WIFI_PASSWORD)
  while not sta_if.isconnected():
    print(".", end="")
    time.sleep(0.1)
  print(" Connected!")
        

connect_wifi() # Connecting to WiFi Router  


client = MQTTClient(client_id=mqtt_client_id, 
                    server=ADAFRUIT_IO_URL, 
                    user=ADAFRUIT_USERNAME, 
                    password=ADAFRUIT_IO_KEY,
                    ssl=False)
try:            
    client.connect()
except Exception as e:
    print('could not connect to MQTT server {}{}'.format(type(e).__name__, e))
    sys.exit()

temp_feed = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, TEMP_FEED_ID), 'utf-8') # format - techiesms/feeds/temp
hum_feed = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, HUM_FEED_ID), 'utf-8') # format - techiesms/feeds/hum   
toggle_feed_1 = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, TOGGLE_FEED_ID_1), 'utf-8') # format - techiesms/feeds/ar
toggle_feed_2 = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, TOGGLE_FEED_ID_2), 'utf-8') # format - techiesms/feeds/geladeira
toggle_feed_3 = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, TOGGLE_FEED_ID_3), 'utf-8') # format - techiesms/feeds/motor
toggle_feed_4 = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, TOGGLE_FEED_ID_4), 'utf-8') # format - techiesms/feeds/motor
toggle_feed_5 = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, TOGGLE_FEED_ID_5), 'utf-8') # format - techiesms/feeds/motor
client.set_callback(cb)
# client.set_callback(rele1_cb)
# client.set_callback(rele2_cb)               
client.subscribe(toggle_feed_1) # Subscribing to particular topic
client.subscribe(toggle_feed_2)
client.subscribe(toggle_feed_3)
client.subscribe(toggle_feed_4)
client.subscribe(toggle_feed_5)
client.subscribe(temp_feed)
client.subscribe(hum_feed)

client.publish(temp_feed,bytes("0", 'utf-8'),qos=0)   # Publishing Temprature to adafruit.ioqos=0)
client.publish(hum_feed,bytes("0", 'utf-8'),qos=0)   # Publishing humity to adafruit.ioqos=0)

def sens_data(data):
    
    sensor.measure()                    # Measuring 
    temp = sensor.temperature()         # getting Temp
    hum = sensor.humidity()
    client.publish(temp_feed,    
                  bytes(str(temp), 'utf-8'),   # Publishing Temprature to adafruit.io
                  qos=0)
    
    client.publish(hum_feed,    
                  bytes(str(hum), 'utf-8'),   # Publishing Temprature to adafruit.io
                  qos=0)
    print("Temp - ", str(temp))
    print("Hum - " , str(hum))
    print('Msg sent')
    
timer = Timer(0)
timer.init(period=5000, mode=Timer.PERIODIC, callback = sens_data)

while True:
    try:
        client.check_msg()
        # if button.value() == 0:  # Botão pressionado
        #     if porta == 0: #Se a porta estiver fechada vamos abrir
        #         print("Botão pressionado! Abrindo a porta...")
        #         # Movendo o servo para 180 graus
        #         motor.move(90)
        #         sleep(1)
        #         porta = 1 #Porta Aberta
        #         continue

        #     else:
        #         print("Botão pressionado! Fechando a porta...")
        #         # Movendo o servo para 0 graus
        #         motor.move(0)
        #         sleep(1)
        #         porta = 0 #Porta Aberta
        #         continue                  # non blocking function
    except :
        client.disconnect()
        sys.exit()
