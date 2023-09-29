RELE1_PIN = 25 #Ar Condicionado
RELE2_PIN = 26 #Geladeira
rele1 = machine.Pin(RELE1_PIN, machine.Pin.OUT)
rele2 = machine.Pin(RELE2_PIN, machine.Pin.OUT)

def rele1_cb(topic, msg):                             # Callback function
    print('Received Data:  Topic = {}, Msg = {}'.format(topic, msg))
    recieved_data = str(msg,'utf-8')            #   Recieving Data
    if recieved_data=="0":
        rele1.value(0)
    if recieved_data=="1":
        rele1.value(1)

def rele2_cb(topic, msg):                             # Callback function
    print('Received Data:  Topic = {}, Msg = {}'.format(topic, msg))
    recieved_data = str(msg,'utf-8')            #   Recieving Data
    if recieved_data=="0":
        rele2.value(0)
    if recieved_data=="1":
        rele2.value(1)