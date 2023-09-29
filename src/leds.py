from lib.i2c_lcd import I2cLcd
from lib.lcd_api import LcdApi
import time

LCD_ENTRADA = 0x26 #Entrada
LCD_SOTAO = 0x27 #Sotao
totalRows = 2
totalColumns = 16
i2c = SoftI2C(scl = Pin(22), sda = Pin(21), freq = 10000)
lcd_entrada = I2cLcd(i2c,LCD_ENTRADA,totalRows,totalColumns)
lcd_sotao = I2cLcd(i2c,LCD_SOTAO,totalRows,totalColumns)

def lcd_entrada_cb(topic,msg):
    print('Received Data:  Topic = {}, Msg = {}'.format(topic, msg))
    recieved_data = str(msg,'utf-8')            #   Recieving Data
    if recieved_data=="0":
        lcd_entrada.clear()
    if recieved_data=="1":
        while recieved_data=="1":
            lcd_entrada.putstr("Bem-Vindo!") #Monstra na Entrada
            time.sleep(2)
            lcd_entrada.clear()

def lcd_sotao_cb(topic,msg):
    print('Received Data:  Topic = {}, Msg = {}'.format(topic, msg))
    recieved_data = str(msg,'utf-8')            #   Recieving Data
    if recieved_data=="0":
        lcd_sotao.clear()
    if recieved_data=="1":
        while recieved_data=="1":
            lcd_sotao.putstr("Hoje está quente!") #Monstra na Entrada
            time.sleep(2)
            lcd_sotao.clear()