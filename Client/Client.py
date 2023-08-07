import socket

def send_file(filename):
    with open(filename, 'rb') as f:
        data = f.read(1024)
        while data:
            client_socket.sendto(data, (HOST, PORT))
            last_data = data
            data = f.read(1024)
            if not data:
                client_socket.sendto(b"<end>", (HOST, PORT))
    print(f"Arquivo {filename} enviado com sucesso!")

# Configurações do cliente
HOST = 'localhost'
PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    action = input("Digite 'enviar' para enviar um arquivo ou 'receber' para receber um arquivo (ou 'exit' para sair): ").lower()

    if action == 'exit':
        client_socket.sendto(action.encode(), (HOST, PORT))
        print("Cliente encerrado.")
        break

    if action == 'enviar':
        filename = input("Digite o nome do arquivo a ser enviado: ")
        client_socket.sendto(f"{action} {filename}".encode(), (HOST, PORT))
        send_file(filename)

    elif action == 'receber':
        filename = input("Digite o nome do arquivo a ser recebido: ")
        client_socket.sendto(f"{action} {filename}".encode(), (HOST, PORT))

        with open(filename, 'wb') as f:
            while True:
                data, addr = client_socket.recvfrom(1024)
                if data == b"File Not Found":
                    print("Arquivo não encontrado no servidor.")
                    break
                if data == b"<end>":
                    print(f"Arquivo {filename} recebido com sucesso.")
                    break
                if data != b'':
                    f.write(data)




    else:
        print("Opção inválida. Tente novamente.")

client_socket.close()
