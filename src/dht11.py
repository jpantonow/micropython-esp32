import machine
import time
import dht

#dht11 = dht22

temperatura = 0
humidade = 0
#Declara onde esta conectado o sensor DHT22
sensor = dht.DHT22(machine.Pin(15))

rele = machine.Pin(2, machine.Pin.OUT)

def medir():
    #Fazer as medições
    sensor.measure()

    #Pegar os valores de tem e hum
    temperatura = sensor.temperature()
    humidade = sensor.humidity()

    return temperatura, humidade




#Loop infinito
while True:
    temperatura, humidade = medir()
    print(f"A temperatura medida é: {temperatura} e a humidade é {humidade}")
    time.sleep(1)
    if temperatura > 25:
        rele.value(1)
    else:
        rele.value(0)

