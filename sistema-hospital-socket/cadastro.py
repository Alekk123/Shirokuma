import socket
import json

HOST = 'localhost'
PORT = 5003

# Inicia o socket 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST, PORT))
s.listen()


print('Cadastro iniciado e esperando por conexões.')

while True:
    # Espera por uma conexão
    conn, addr = s.accept()
    print(f'Conectado por {addr}')

    # Recebe os dados do cliente
    print('recebendo')

    user_type = conn.recv(1024).decode().strip()
    if user_type == '1':
        data = conn.recv(1024).decode().strip()
        name, cpf = data.split(';')
        print(f'Dados recebidos: Nome = {name}, CPF = {cpf}, tipo = {user_type}')
    elif user_type == '2':
        data = conn.recv(1024).decode().strip()
        name, cpf, crm, especialidade = data.split(';')
        print(f'Dados recebidos: Nome = {name}, CPF = {cpf}, tipo = {user_type}, crm = {crm}, especialidade = {especialidade}')
    
    else:
        crm = None
        especialidade = None

    # Realiza o processamento dos dados do cliente, como salvar no banco de dados

    # Envia uma resposta ao servidor principal
    response = 'Dados recebidos e processados com sucesso!'
    conn.sendall(response.encode())
    
    #conn.close() 
