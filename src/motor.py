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

while True:
    if button.value() == 0:  # Botão pressionado
      if porta == 0: #Se a porta estiver fechada vamos abrir
        print("Botão pressionado! Abrindo a porta...")
        # Movendo o servo para 180 graus
        motor.move(90)
        sleep(1)
        porta = 1 #Porta Aberta

      else:
        print("Botão pressionado! Fechando a porta...")
        # Movendo o servo para 0 graus
        motor.move(0)
        sleep(1)
        porta = 0 #Porta Aberta



#Referências
## https://www.upesy.com/blogs/tutorials/esp32-servo-motor-sg90-on-micropython