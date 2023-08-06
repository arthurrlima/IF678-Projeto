import socket
import select

UDP_IP = "127.0.0.1"
IN_PORT = 5005
timeout = 3


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, IN_PORT))

while True:
    print ("Aguardando Conexao...")
    data, addr = sock.recvfrom(1024)
    if data:
        print ("Recebendo arquivo: ")
        print ("File name:", data.decode('ascii'))
        file_name = data.strip()

    f = open("sv_files/demofile.txt", 'x')

    while True:
        ready = select.select([sock], [], [], timeout)
        if ready[0]:
            data, addr = sock.recvfrom(1024)
            f.write(data.decode('ascii'))
        else:
            print ("%s Finish!" % file_name)
            f.close()
            break