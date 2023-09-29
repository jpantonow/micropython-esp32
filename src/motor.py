#Garagem de Bike
from machine import Pin, PWM
from servo import Servo
from time import sleep

# Definindo os pinos
motor = Servo(pin=13) # Pino onde o servo está conectado
button_pin = 14 # Pino onde o botão está conectado
porta = 0       #0 => Fechada; 1 => Aberta

# Configurando o botão
button = Pin(button_pin, Pin.IN, Pin.PULL_UP)

# Posição inicial do servo
motor.move(0)

def ligar_motor_cb(topic,msg):
    print('Received Data:  Topic = {}, Msg = {}'.format(topic, msg))
    recieved_data = str(msg,'utf-8')            #   Recieving Data
    if recieved_data=="0":
        while recieved_data=="0":
          if button.value() == 0:  # Botão pressionado
            if porta == 0: #Se a porta estiver fechada vamos abrir
              #print("Botão pressionado! Abrindo a porta...")
              # Movendo o servo para 180 graus
              motor.move(90)
              sleep(1)
              porta = 1 #Porta Aberta
              motor.move(0)
        while recieved_data=="1":
           
    if recieved_data=="1":
        motor.move(0)
        sleep(1)
        porta = 0

client.set_callback(ligar_motor_cb)  
