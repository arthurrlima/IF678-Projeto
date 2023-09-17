import socket

def make_pkt(file):
    return file.read(1024)

def udp_send(packet, data, client_socket):
    client_socket.sendto(data, packet)

def extract(client_socket):
    data, addr = client_socket.recvfrom(1024)
    return data, addr

def deliver_data(file, data):
    return file.write(data)





def send_file(filename, client_socket, packet):
    with open(filename, 'rb') as f:
        data = make_pkt(f)

        while data:

            udp_send(packet, data, client_socket)
            data = make_pkt(f)

            if not data:
                udp_send(packet, b"<end>", client_socket)
    print(f"Arquivo {filename} enviado com sucesso!")

#rtd_rcv(packet)
def recive_file(filename, client_socket):


    with open(filename, 'wb') as f:
            while True:
                # extract(packet, data)
                data, addr = extract(client_socket)
                if data == b"File Not Found":
                    print("Arquivo não encontrado no servidor.")
                    break
                if data == b"<end>":
                    print(f"Arquivo {filename} recebido com sucesso.")
                    break

                elif data != b'':
                    deliver_data(f, data)

# Configurações do cliente
HOST = 'localhost'
PORT = 12345


packet = (HOST, PORT)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    action = input("Digite 'enviar' para enviar um arquivo ou 'receber' para receber um arquivo (ou 'exit' para sair): ").lower()

    if action == 'exit':
        client_socket.sendto(action.encode(), packet)
        print("Cliente encerrado.")
        break

    if action == 'enviar':
        filename = input("Digite o nome do arquivo a ser enviado: ")
        client_socket.sendto(f"{action} {filename}".encode(), packet)
        send_file(filename, client_socket, packet)

    elif action == 'receber':
        filename = input("Digite o nome do arquivo a ser recebido: ")
        client_socket.sendto(f"{action} {filename}".encode(), packet)
        recive_file(filename, client_socket)

    else:
        print("Opção inválida. Tente novamente.")

client_socket.close()
