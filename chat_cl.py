import socket
import sys
import chat_fx as fx

serverName = "127.0.0.1"  #Enter your IP address here
serverPort = 5005
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSocket.setblocking(0)

while True:
    try:
        message = input("Input sentence:")
        fx.rdt_send(message,serverName,serverPort,clientSocket)
    except KeyboardInterrupt as ee:
        sys.exit(1)
clientSocket.close()