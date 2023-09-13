import socket      
import chat_fx as fx


#AF_INET used for IPv4
#SOCK_DGRAM used for UDP protocol
UDP_IP = "127.0.0.1"
IN_PORT = 5005
timeout = 3


serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSock.bind((UDP_IP, IN_PORT))
svip, svport = serverSock.getsockname()
print("Server started ..."+svip, svport)
print("Waiting for Clients...") 
#receiving data from client

ackseq=-1
req=0
messg=''

while True:
    try:
        payload, clientAddress = serverSock.recvfrom(1024)
        clientIP, clientPort = clientAddress
        payload = payload.decode()
    
        if payload=="/r/r":
            print(clientIP,':',clientPort,'/~user: ',messg, sep='')
            print('')
            ackseq=-1
            req=0
            messg=''
            continue
        payload=payload.split('/r')
        checksumm=[]
        checksumm.append(list(fx.calculate_checksum(payload[0].split())))
        checksumm.append(list(payload[1]))
        sum=fx.summ(checksumm)
        if ('0' not in sum) and (req==int(payload[2])):
            if req==0:
                req=1
                ackseq=0
            else :
                req=0
                ackseq=1
            messg+=payload[0]
            modifiedpayload = 'AK'+'/r'+'1011111010110100'+'/r'+payload[2]
            print("from:",clientAddress, "ACK: "+payload[2])
            serverSock.sendto(modifiedpayload.encode(), clientAddress)
        elif ('0' in sum) or (req!=int(payload[2])):
            modifiedpayload = 'AK'+'/r'+'1011111010110100'+'/r'+str(ackseq)
            print("from:",clientAddress, "ACK: "+ackseq)
            serverSock.sendto(modifiedpayload.encode(), clientAddress)
    except KeyboardInterrupt as e:
        sys.exit()
serverSock.close()



