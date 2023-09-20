import socket
import hashlib
import struct

#função que adiciona bytes nulos ao final do arquivo para que ele tenha 1024 bytes
def to_1024_bytes(data):
    if len(data) < 1024:
        #adiciona bytes nulos ao final do arquivo para que ele tenha 1024 bytes
        data += b'\x00' * (1024 - len(data))
    return data

#função que gera o pacote
def make_pkt(file, expected_seq):
    data = file.read(1024)
    end = False
    if len(data) < 1024:
        #adiciona bytes nulos ao final do arquivo para que ele tenha 1024 bytes
        data += b'\x00' * (1024 - len(data))
        end = True
    checksum = hashlib.md5(data).digest()
    # cria um pacote de 1028 bytes, sendo os 4 primeiros bytes o checksum e os 1024 bytes restantes o arquivo
    packet = struct.pack('<16s1024s1s', checksum, data, expected_seq)
    print(" pacote: ", packet)
    return packet, end

#função que extrai o pacote
def extract(server_socket):
    data, addr = server_socket.recvfrom(1041)
    checksum , data, seq_recived = struct.unpack('<16s1024s1s', data)
    return checksum, data, seq_recived

#função que envia o pacote
def udp_send(server_socket, data, client_address):
    server_socket.sendto(data, client_address)

#função que escreve o arquivo
def deliver_data(file, data):
    return file.write(data)

#função que verifica se o pacote é um ACK
def isACK(client_socket):
    data, addr = client_socket.recvfrom(4)
    data, rcv_seq = struct.unpack('<3s1s', data)
    if data == b"ACK":
        return True, rcv_seq
    else:
        return False, rcv_seq

#função que verifica se o pacote está corrompido
def check_checksum(checksum, data):
    md5 = hashlib.md5(data).digest()
    if  checksum == md5:
        return True
    else:
        return False

#função que muda a sequencia do pacote
def change_seq(seq):
    if seq == b'0':
        return b'1'
    else:
        return b'0'


# rtd_send(data)
def send_file(filename, client_address, server_socket):

    try:
        with open(filename, 'rb') as f:

            # dicionário que armazena os pacotes 0 e 1
            pac_order = {}
            espected_seq = b'0'
            # gera o pacote
            packet, end = make_pkt(f, espected_seq)

            # armazena o pacote 0 no dicionário
            pac_order[espected_seq] = (packet, end)

            while packet:

                # envia o pacote
                udp_send(server_socket, packet, client_address)

                # verifica se o pacote foi corrompido ou se está fora de ordem
                is_ack, rcv_seq = isACK(server_socket)

                while not is_ack:

                    # caso o pacote esteja fora de ordem pega o pacote correto
                    if espected_seq != rcv_seq:
                        print("Pacote fora de ordem.")
                        print("Reenviando pacote...\n")
                        espected_seq = change_seq(espected_seq)
                        packet, end = pac_order[espected_seq]

                    # caso o pacote esteja corrompido
                    else:
                        print("Pacote corrompido.")
                        print("Reenviando pacote...\n")

                    # reenvia o pacote correto
                    udp_send(server_socket, packet, client_address)
                    is_ack, rcv_seq = isACK(server_socket)

                # muda a sequencia do pacote esperado
                espected_seq = change_seq(espected_seq)

                # caso o pacote seja o último
                if end:

                    # envia o pacote
                    packet = struct.pack('<16s1024s1s', hashlib.md5(b"<end>").digest(), b"<end>", espected_seq)
                    udp_send(server_socket, packet, client_address)
                    is_ack, rcv_seq = isACK(server_socket)

                    # verifica se o pacote foi corrompido ou se está fora de ordem
                    while not is_ack:
                        # caso o pacote esteja fora de ordem pega o pacote correto
                        if espected_seq != rcv_seq:
                            print("Pacote fora de ordem.")
                            print("Reenviando pacote...\n")
                            espected_seq = change_seq(espected_seq)
                            packet, end = pac_order[espected_seq]

                        # caso o pacote esteja corrompido
                        else:
                            print("Pacote corrompido.")
                            print("Reenviando pacote...\n")
                        udp_send(server_socket, packet, client_address)
                        is_ack, rcv_seq = isACK(server_socket)
                    break
                # gera o próximo pacote
                packet, end = make_pkt(f, espected_seq)
                pac_order[espected_seq] = (packet, end)

    except FileNotFoundError:
        print("Arquivo não encontrado no servidor.")
        packet = struct.pack('<16s1024s', hashlib.md5(b"File Not Found").digest(), b"File Not Found", 2)
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

        #inicio da sequencia de pacotes
        espected_seq = b'0'
        while True:
            #recebe o pacote
            checksum, data, seq_recived = extract(server_socket)

            #verifica se o pacote recebido é o esperado
            if seq_recived != espected_seq:
                #envia o NAK
                print("Pacote fora de ordem.")
                print("Reenviando pacote...\n")
                packet = struct.pack('<3s1s',b"NAK", espected_seq)
                udp_send(server_socket, packet, client_address)
                continue

            else:

                #verifica se o arquivo foi encontrado no cliente
                if data == to_1024_bytes(b"File Not Found"):
                    print("Arquivo não encontrado no servidor.")
                    break

                #verifica se o arquivo chegou ao fim
                elif data == to_1024_bytes(b"<end>"):

                    #envia o ACK
                    packet = struct.pack('<3s1s',b"ACK", espected_seq)
                    udp_send(server_socket, packet, client_address)

                    print("Arquivo recebido com sucesso.")
                    break

                #verifica se o pacote não está corrompido
                elif check_checksum(checksum, data):
                    #envia o ACK
                    print("Pacote", data, "recebido com sucesso")
                    packet = struct.pack('<3s1s',b"ACK", espected_seq)
                    udp_send(server_socket, packet, client_address)

                    #escreve o pacote no arquivo
                    deliver_data(f, data)

                    #muda a sequencia do pacote esperado
                    espected_seq = change_seq(espected_seq)

                #caso o pacote esteja corrompido
                else:
                    #envia o NAK
                    print("Pacote corrompido.")
                    print("Reenviando pacote...\n")
                    packet = struct.pack('<3s1s', b"NAK", espected_seq)
                    udp_send(server_socket, packet, client_address)







HOST = 'localhost'
PORT = 12345
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

print(f"Servidor UDP iniciado em {HOST}:{PORT}")

while True:
    data, client_address = server_socket.recvfrom(1041)
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
