from lib.i2c_lcd import I2cLcd
from lib.lcd_api import LcdApi
import time
class Leds:
    def __init__(self):
        LCD_ENTRADA = 0x26 #Entrada
        LCD_SOTAO = 0x27 #Sotao
        totalRows = 2
        totalColumns = 16
        self.i2c = SoftI2C(scl = Pin(22), sda = Pin(21), freq = 10000)
        self.lcd_entrada = I2cLcd(i2c,LCD_ENTRADA,totalRows,totalColumns)
        self.lcd_sotao = I2cLcd(i2c,LCD_SOTAO,totalRows,totalColumns)
    def executar():
        while True:
             lcd_entrada.putstr("Bem-Vindo!") #Monstra na Entrada
             time.sleep(2)
             lcd_entrada.clear()
             lcd_sotao.putstr("Hoje está quente!") #Mostra no Sotão
             time.sleep(2)
             lcd_sotao.clear()