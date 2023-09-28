import machine
import time
import dht

#dht11 = dht22

temperatura = 0
humidade = 0
#Declara onde esta conectado o sensor DHT22
sensor = dht.DHT22(machine.Pin(12))


def medir():
    #Fazer as medições
    sensor.measure()

    #Pegar os valores de tem e hum
    temperatura = sensor.temperature()
    humidade = sensor.humidity()

    return temperatura, humidade



