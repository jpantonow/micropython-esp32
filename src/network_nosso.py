from machine import Pin, Timer
import network
import time
from umqtt.robust import MQTTClient
import sys #Utilizado para terminar o programa
import dht

sensor = dht.DHT22(Pin(15))                  # DHT11 Sensor on Pin 4 of ESP32

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


def cb(topic, msg):                             # Callback function
    print('Received Data:  Topic = {}, Msg = {}'.format(topic, msg))
    recieved_data = str(msg,'utf-8')            #   Recieving Data
    if recieved_data=="0":
        led.value(0)
    if recieved_data=="1":
        led.value(1)
        
temp_feed = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, TEMP_FEED_ID), 'utf-8') # format - techiesms/feeds/temp
hum_feed = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, HUM_FEED_ID), 'utf-8') # format - techiesms/feeds/hum   
toggle_feed_1 = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, TOGGLE_FEED_ID_1), 'utf-8') # format - techiesms/feeds/ar
toggle_feed_2 = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, TOGGLE_FEED_ID_2), 'utf-8') # format - techiesms/feeds/geladeira
toggle_feed_3 = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, TOGGLE_FEED_ID_3), 'utf-8') # format - techiesms/feeds/motor
toggle_feed_4 = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, TOGGLE_FEED_ID_4), 'utf-8') # format - techiesms/feeds/motor
toggle_feed_5 = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, TOGGLE_FEED_ID_5), 'utf-8') # format - techiesms/feeds/motor

client.set_callback(cb)      # Callback function               
client.subscribe(toggle_feed_1) # Subscribing to particular topic
client.subscribe(toggle_feed_2)
client.subscribe(toggle_feed_3)
client.subscribe(toggle_feed_4)
client.subscribe(toggle_feed_5)
client.subscribe(temp_feed)
client.subscribe(hum_feed)

client.publish(temp_feed,bytes(str(temp), 'utf-8'),qos=0)   # Publishing Temprature to adafruit.ioqos=0)
client.publish(hum_feed,bytes(str(hum), 'utf-8'),qos=0)   # Publishing humity to adafruit.ioqos=0)

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
        client.check_msg()                  # non blocking function
    except :
        client.disconnect()
        sys.exit()
