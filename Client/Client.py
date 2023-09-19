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
    checksum, data = struct.unpack('<16s1024s', data)
    return checksum, data

def udp_send(packet, data, client_socket):
    client_socket.sendto(data, packet)

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






def send_file(filename, client_socket, dest_address):
    try:
        with open(filename, 'rb') as f:

            #gera o pacote
            packet, end = make_pkt(f)

            while packet:

                #envia o pacote
                udp_send(dest_address, packet, client_socket)

                #verifica se o pacote foi corrompido
                is_ack = isACK(client_socket)
                while not is_ack:
                    print("Pacote corrompido.")
                    print("Reenviando pacote...\n")
                    #reenvia o pacote caso tenha sido corrompido até que seja recebido um ACK
                    udp_send(dest_address, packet, client_socket)
                    is_ack = isACK(client_socket)

                if end:
                    packet = struct.pack('<16s1024s', hashlib.md5(b"<end>").digest(), b"<end>")
                    udp_send(dest_address, packet, client_socket)
                    is_ack = isACK(client_socket)
                    while not is_ack:
                        print("Pacote corrompido.")
                        print("Reenviando pacote...\n")
                        udp_send(dest_address, packet, client_socket)
                        is_ack = isACK(client_socket)
                    break

                packet, end = make_pkt(f)



    except FileNotFoundError:
        print("Arquivo não encontrado no servidor.")


#rtd_rcv(packet)
def receive_file(filename, client_socket, dest_address):

    with open(filename, 'wb') as f:
            while True:

                # extract(packet, data)
                checksum, data = extract(client_socket)

                if data == to_1024_bytes(b"File Not Found"):
                    print("Arquivo não encontrado")
                    break

                elif data == to_1024_bytes(b"<end>"):
                    packet = b"ACK"
                    udp_send(dest_address, packet, client_socket)
                    deliver_data(f, data)
                    print("Arquivo recebido com sucesso.")
                    break

                elif check_checksum(checksum, data):
                    print("Pacote", data, "recebido com sucesso")
                    packet = b"ACK"
                    udp_send(dest_address, packet, client_socket)
                    deliver_data(f, data)

                else:
                    print("Pacote corrompido.")
                    print("Reenviando pacote...\n")
                    packet = b"NAK"
                    udp_send(dest_address, packet, client_socket)



# Configurações do cliente
HOST = 'localhost'
PORT = 12345




dest_address  = (HOST, PORT)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    action = input("Digite 'enviar' para enviar um arquivo ou 'receber' para receber um arquivo (ou 'exit' para sair): ").lower()

    if action == 'exit':
        client_socket.sendto(action.encode(), dest_address)
        print("Cliente encerrado.")
        break

    if action == 'enviar':
        filename = input("Digite o nome do arquivo a ser enviado: ")
        client_socket.sendto(f"{action} {filename}".encode(), dest_address)
        send_file(filename, client_socket, dest_address)

    elif action == 'receber':
        filename = input("Digite o nome do arquivo a ser recebido: ")
        client_socket.sendto(f"{action} {filename}".encode(), dest_address)
        receive_file(filename, client_socket, dest_address)

    else:
        print("Opção inválida. Tente novamente.")

client_socket.close()
