#Cozinha
from machine import Pin, ADC
from time import sleep, time

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

while True:
    # Ler valor do ADC
    adc_value = mq135.read()
    
    # Calcular a concentração de CO2 em ppm
    co2_ppm = calculate_ppm(adc_value, calibration_avg)
    
    # Reportar qualidade do ar
    print("Leitura ADC: {}, Concentração de CO2: {:.2f} ppm".format(adc_value, co2_ppm))
    
    # Verificar níveis anormais de CO2 (indicador de incêndio)
    if co2_ppm > co2_ppm*1.5: #5000:  # O limite pode variar dependendo do ambiente
        #print("Nível de CO2 anormalmente alto! Possível incêndio!")
        led.on()  # Acender o LED interno
    else:
        led.off()  # Apagar o LED interno

    sleep(5)  # Espera por 5 segundos antes da próxima leitura