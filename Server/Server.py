import socket

def receive_file(filename, client_address):
    with open(filename, 'wb') as f:
        while True:
            data, addr = server_socket.recvfrom(1024)
            if data == b"<end>":
                break
            if addr == client_address and data != b'':
                f.write(data)

    print(f"Arquivo {filename} recebido com sucesso!")

# Configurações do servidor
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
        receive_file(filename, client_address)
    elif action.lower() == 'receber':
        try:
            with open(filename, 'rb') as f:
                data = f.read(1024)
                while data:
                    server_socket.sendto(data, client_address)
                    last_data = data
                    data = f.read(1024)
                    if not data:
                        server_socket.sendto(b"<end>", client_address)

            print(f"Arquivo {filename} enviado para o cliente.")
        except FileNotFoundError:
            server_socket.sendto(b"File Not Found", client_address)
    else:
        print(f"Comando inválido: {data}")

server_socket.close()
