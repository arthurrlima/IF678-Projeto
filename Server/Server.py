import socket
import hashlib
import struct

def to_1024_bytes(data):
    if len(data) < 1024:
        #adiciona bytes nulos ao final do arquivo para que ele tenha 1024 bytes
        data += b'\x00' * (1024 - len(data))
    return data

def make_pkt(file):
    data = file.read(1024)
    end = False
    if len(data) < 1024:
        #adiciona bytes nulos ao final do arquivo para que ele tenha 1024 bytes
        data += b'\x00' * (1024 - len(data))
        end = True
    checksum = hashlib.md5(data).digest()
    # cria um pacote de 1028 bytes, sendo os 4 primeiros bytes o checksum e os 1024 bytes restantes o arquivo
    packet = struct.pack('<16s1024s', checksum, data)
    print(" pacote: ", packet)
    return packet, end


def extract(server_socket):
    data, addr = server_socket.recvfrom(1040)
    checksum , data = struct.unpack('<16s1024s', data)
    return checksum, data


def udp_send(server_socket, data, client_address):
    server_socket.sendto(data, client_address)


def deliver_data(file, data):
    return file.write(data)

def isACK(client_socket):
    data, addr = client_socket.recvfrom(1040)
    if data == b"ACK":
        return True
    else:
        return False

def check_checksum(checksum, data):
    md5 = hashlib.md5(data).digest()
    if  checksum == md5:
        return True
    else:
        return False

# rtd_send(data)
def send_file(filename, client_address, server_socket):

    try:
        with open(filename, 'rb') as f:

            packet, end = make_pkt(f)

            while packet:

                udp_send(server_socket, packet, client_address)

                is_ack = isACK(server_socket)

                while not is_ack:
                    print("Pacote corrompido.")
                    print("Reenviando pacote...\n")
                    udp_send(server_socket, packet, client_address)
                    is_ack = isACK(server_socket)

                if end:
                    packet = struct.pack('<16s1024s', hashlib.md5(b"<end>").digest(), b"<end>")
                    udp_send(server_socket, packet, client_address)
                    is_ack = isACK(server_socket)
                    while not is_ack:
                        print("Pacote corrompido.")
                        print("Reenviando pacote...\n")
                        udp_send(server_socket, packet, client_address)
                        is_ack = isACK(server_socket)
                    break

                packet, end = make_pkt(f)



    except FileNotFoundError:
        print("Arquivo não encontrado no servidor.")
        packet = struct.pack('<16s1024s', hashlib.md5(b"File Not Found").digest(), b"File Not Found")
        udp_send(server_socket, packet, client_address)
        is_ack = isACK(server_socket)
        while not is_ack:
            print("Pacote corrompido.")
            print("Reenviando pacote...\n")
            udp_send(server_socket, packet, client_address)
            is_ack = isACK(server_socket)

# rtd_rcv(packet)
def receive_file(filename, client_address, server_socket):

    with open(filename, 'wb') as f:
        while True:

            checksum, data = extract(server_socket)

            if data == to_1024_bytes(b"File Not Found"):
                print("Arquivo não encontrado no servidor.")
                break


            elif data == to_1024_bytes(b"<end>"):
                packet = b"ACK"
                udp_send(server_socket, packet, client_address)
                deliver_data(f, data)
                print("Arquivo recebido com sucesso.")
                break


            elif check_checksum(checksum, data):
                print("Pacote", data, "recebido com sucesso")
                packet = b"ACK"
                udp_send(server_socket, packet, client_address)
                deliver_data(f, data)
            else:
                print("Pacote corrompido.")
                print("Reenviando pacote...\n")
                packet = b"NAK"
                udp_send(server_socket, packet, client_address)





HOST = 'localhost'
PORT = 12345
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

print(f"Servidor UDP iniciado em {HOST}:{PORT}")

while True:
    data, client_address = server_socket.recvfrom(1040)
    data = data.decode()

    if data.lower() == "exit":
        print("Servidor encerrado.")
        break

    action, filename = data.split()
    if action.lower() == 'enviar':
        receive_file(filename, client_address, server_socket)

    elif action.lower() == 'receber':
        send_file(filename, client_address, server_socket)

server_socket.close()
