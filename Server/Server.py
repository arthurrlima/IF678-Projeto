import socket


def make_pkt(file):
    return file.read(1024)


def extract(server_socket):
    data, addr = server_socket.recvfrom(1024)
    return data, addr


def udp_send(server_socket, data, client_address):
    server_socket.sendto(data, client_address)


def deliver_data(file, data):
    return file.write(data)


# rtd_send(data)
def send_file(filename, client_address, server_socket):
    try:
        with open(filename, 'rb') as f:
            data = make_pkt(f)

            while data:

                # udp_send(packet, data)
                udp_send(server_socket, data, client_address)
                data = make_pkt(f)

                if not data:
                    udp_send(server_socket, b"<end>", client_address)
        print(f"Arquivo {filename} enviado para o cliente.")

    except FileNotFoundError:
        print("Arquivo não encontrado no servidor.")
        udp_send(server_socket, b"File Not Found", client_address)


# rtd_rcv(packet)
def receive_file(filename, client_address, server_socket):
    with open(filename, 'wb') as f:
        while True:
            data, addr = extract(server_socket)

            if data == b"<end>":
                break

            if addr == client_address and data != b'':
                deliver_data(f, data)

    print(f"Arquivo {filename} recebido com sucesso!")


HOST = 'localhost'
PORT = 12345
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

print(f"Servidor UDP iniciado em {HOST}:{PORT}")

while True:
    data, client_address = server_socket.recvfrom(1024)
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
