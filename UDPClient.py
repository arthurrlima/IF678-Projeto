import socket
import time
import sys

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
buf = 1024
file_name = "demofile.txt"

f = open(file_name, "r")
data = f.read(buf)

UDPClient_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPClient_sock.sendto(file_name.encode(), (UDP_IP, UDP_PORT))

print ("Conexão Estabelecida! adress: "+UDP_IP)
print ("Enviando %s ..." % file_name)


while(data):
    if(UDPClient_sock.sendto(data.encode(), (UDP_IP, UDP_PORT))):
        data = f.read(buf)
        time.sleep(0.02) # Delay antes de fechar o arquivo
f.close()

#Recebendo Arquivo de volta.
receivedBytes, adress  = UDPClient_sock.recvfrom(buf)

#Salvando Arquivo recebido.
f2 = open("cl_files/"+file_name, 'x')
f2.write(receivedBytes.decode('ascii'))
f2.close
print ("Arquivo Recebido.")

UDPClient_sock.close()
print ("Conexão Encerrada.")
