import socket
import time
import sys

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
buf = 1024
file_name = "demofile.txt"

f = open(file_name, "r")
data = f.read(buf)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(file_name.encode(), (UDP_IP, UDP_PORT))

print ("Conexão Estabelecida! adress: "+UDP_IP)
print ("Enviando %s ..." % file_name)


while(data):
    if(sock.sendto(data.encode(), (UDP_IP, UDP_PORT))):
        data = f.read(buf)
        time.sleep(0.02) # Delay antes de fechar o socket

sock.close()
f.close()