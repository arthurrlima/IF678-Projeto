import socket      

#AF_INET used for IPv4
#SOCK_DGRAM used for UDP protocol
UDP_IP = "127.0.0.1"
IN_PORT = 5005
timeout = 3


serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSock.bind((UDP_IP, IN_PORT))
svip, svport = serverSock.getsockname()
print("Server started ..."+svip, svport)
print("Waiting for Client response...") 
#receiving data from client




while True:
    payload, address = serverSock.recvfrom(1024)
    
    print(address,"user:", payload.decode('ascii'))