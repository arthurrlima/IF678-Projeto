import socket

#client program

import time
import sys
import select

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
buf = 1024
file_name = "demofile32.jpg"
timeout = 3

f = open(file_name, "rb")
#data = f.read(buf)

msg = "HI! this is automsg!"


clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSock.sendto(msg.encode(), (UDP_IP, UDP_PORT))

while True:
       m = input("Enter data to send server: ")
       res = clientSock.sendto(m.encode(),(UDP_IP,UDP_PORT)) 
       if res:
          print("\nsuccessfully send")
    