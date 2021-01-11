'''
Alunos: Carlos Henrique, João Victor Voltarelli
Disciplina: Gerência de Redes

'''

import socket
import time
import paho.mqtt.client as clienteMQTT #FOI NECESSARIO UTILIZAR: pip install paho-mqtt

def on_connect(client, userdata, flags, rc):
 
    if rc == 0:
        print("Conectado ao broker!\n")
        global Connected               
        Connected = True                
 
    else:
        print("Conexao falhou!")

#INFORMACOES DO BROKER
broker = "192.168.0.104" #LOCALHOST
porta = 1883
topico = "gerencia/temperatura"

client = clienteMQTT.Client(protocol=clienteMQTT.MQTTv31)
client.on_connect = on_connect
client.connect(broker, port=porta)
client.loop_start()

Connected = False #CONTROLE DA CONEXAO COM O BROKER

while Connected != True: #ESPERA PELA CONEXAO
    time.sleep(0.1)

#SOCKET UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    #ENVIANDO PARA O HOST
    sock.sendto(b"Enviando!", ("155.138.134.219", 22801))
    #RECEBENDO A RESPOSTA DO HOST
    data, addr = sock.recvfrom (1024)
    resposta = str(data)[2:-1]
    print("Temperatura recebida: ", resposta)

    #PUBLICANDO A TEMPERATURA RECEBIDA NO BROKER
    client.publish(topico, "Temperatura: " + resposta)

    #SLEEP DE 5 SEG PARA RECEBER O PROXIMO DADO
    time.sleep(5)