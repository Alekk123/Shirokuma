import socket

HOST = 'localhost'  # Endereço IP do servidor principal
PORT = 5000  # Porta do servidor principal

# Criação do socket do cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#conexão com o servidor-principal
client_socket.connect((HOST, PORT))
print('Conexão estabelecida com o servidor principal.', PORT)

menu = client_socket.recv(2048).decode().strip()
#print(menu)

escolha = input("> ")
client_socket.sendall(escolha.encode())

if escolha == '1':
    # Primeiro acesso - envia nome e CPF para o servidor principal
    nome = input("Digite seu nome: ")
    cpf = input("Digite seu CPF: ")
    data_nasc = input("Digite sua data de nascimento (DD/MM/AAAA):")

    # Envia os dados para o servidor principal
    client_socket.sendall(nome.encode())
    client_socket.sendall(cpf.encode())
    client_socket.sendall(data_nasc.encode())

    # Recebe a resposta do servidor principal
    resposta = client_socket.recv(1024).decode().strip()
    print(resposta)

 