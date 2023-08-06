import socket
import time
import sys
import select

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
buf = 1024
file_name = "demofile32.jpg"
timeout = 3

f = open(file_name, "rb")
data = f.read(buf)

UDPClient_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPClient_sock.sendto(file_name.encode(), (UDP_IP, UDP_PORT))

print ("Conexão Estabelecida! adress: "+UDP_IP)
print ("Enviando %s ..." % file_name)


while(data):
    if(UDPClient_sock.sendto(data, (UDP_IP, UDP_PORT))):
        data = f.read(buf)
        time.sleep(0.02) # Delay antes de fechar o arquivo
f.close()

#Recebendo Arquivo de volta.
f2 = open("cl_files/"+file_name, 'wb')
while True:
    ready = select.select([UDPClient_sock], [], [], timeout)
    if ready[0]:
        receivedBytes, adress  = UDPClient_sock.recvfrom(buf)
        f2.write(receivedBytes)
    else:
        print("Arquivo Recebido!")
        f2.close()
        break
    

#Salvando Arquivo recebido.
#Fechando Socket
UDPClient_sock.close()
print ("Conexão Encerrada.")
