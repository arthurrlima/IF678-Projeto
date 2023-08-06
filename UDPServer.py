import socket
import select
import time
import sys

UDP_IP = "127.0.0.1"
IN_PORT = 5005
timeout = 3


Server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
Server_sock.bind((UDP_IP, IN_PORT))

while True:
    print ("Aguardando Conexao...")
    data, addr = Server_sock.recvfrom(1024)
    if data:
        print ("Conexão Estabelecida! \n Aguardando Arquivo...")
        print ("Recebendo arquivo: ")
        print ("File name:", data.decode('ascii'))
        file_name = data.strip().decode('ascii')

    f = open("sv_files/"+file_name, 'wb')

    while True:
        ready = select.select([Server_sock], [], [], timeout)
        if ready[0]:
            data, addr = Server_sock.recvfrom(1024)
            f.write(data)
        else:
            print ("%s Finish!" % file_name)
            f.close()
            

            #Devolvendo Arquivo
            print ("Devolvendo Arquivo ao Cliente...")
            f2 = open("sv_files/"+file_name, 'rb')
            data2 = f2.read(1024)

            while(data2):
                if(Server_sock.sendto(data2, addr)):
                    data2 = f2.read(1024)
                    time.sleep(0.02)
            f2.close()
            print ("Arquivo Devolvido!")
            break
        
