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
def make_pkt(msg, expected_seq):
    if len(msg) >= 1024:
        data = msg[:1024] #pega os 1024 primeiros char do arquivo

        #transforma em byte
        data = data.encode()
        msg = msg[1024:]
    else:
        data = msg.encode()
        msg = b""

    if len(data) < 1024:
        #adiciona bytes nulos ao final do arquivo para que ele tenha 1024 bytes
        data += b'\x00' * (1024 - len(data))
    checksum = hashlib.md5(data).digest()
    # cria um pacote de 1028 bytes, sendo os 4 primeiros bytes o checksum e os 1024 bytes restantes o arquivo
    packet = struct.pack('<16s1024s1s', checksum, data, expected_seq)
    print(" pacote: ", packet)
    return packet, msg

#função que extrai o pacote
def extract(server_socket):
    data, addr = server_socket.recvfrom(1041)
    checksum , data, seq_recived = struct.unpack('<16s1024s1s', data)
    return checksum, data, seq_recived

#função que envia o pacote
def udp_send(packet, data, client_socket):
    client_socket.sendto(data, packet)

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


def send_file(msg, client_socket, dest_address):
    try:
            end = True
            #dicionário que armazena os pacotes 0 e 1
            pac_order = {}
            espected_seq = b'0'

            while end:

                # gera o próximo pacote
                if msg == b"":
                    packet, msg = make_pkt('<end>', espected_seq)
                    pac_order[espected_seq] = (packet, msg)
                    end = False

                else:
                    packet, msg = make_pkt(msg, espected_seq)
                    pac_order[espected_seq] = (packet, msg)



                #envia o pacote
                udp_send(dest_address, packet, client_socket)

                #verifica se o pacote foi corrompido ou se está fora de ordem
                is_ack, rcv_seq = isACK(client_socket)

                while not is_ack:

                    #caso o pacote esteja fora de ordem pega o pacote correto
                    if espected_seq != rcv_seq:
                        print("Pacote fora de ordem.")
                        print("Reenviando pacote...\n")
                        espected_seq = change_seq(espected_seq)
                        packet, msg = pac_order[espected_seq]

                    #caso o pacote esteja corrompido
                    else:
                        print("Pacote corrompido.")
                        print("Reenviando pacote...\n")

                    #reenvia o pacote correto
                    udp_send(dest_address, packet, client_socket)
                    is_ack = isACK(client_socket)

                #muda a sequencia do pacote esperado
                espected_seq = change_seq(espected_seq)







    #caso o arquivo não seja encontrado no servidor
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
    #action = input("Digite 'enviar' para enviar um arquivo ou 'receber' para receber um arquivo (ou 'exit' para sair): ").lower()
    action = 'enviar'
    if action == 'exit':
        client_socket.sendto(action.encode(), dest_address)
        print("Cliente encerrado.")
        break

    if action == 'enviar':
        filename = input("Digite o nome do arquivo a ser enviado: ")
        client_socket.sendto(action.encode(), dest_address)
        send_file(filename, client_socket, dest_address)

    elif action == 'receber':
        filename = input("Digite o nome do arquivo a ser recebido: ")
        client_socket.sendto(action.encode(), dest_address)
        receive_file(filename, client_socket, dest_address)

    else:
        print("Opção inválida. Tente novamente.")

client_socket.close()
