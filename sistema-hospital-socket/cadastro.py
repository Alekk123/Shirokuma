import socket

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
    data = conn.recv(1024).decode().strip()
    print('recebendo')
    nome, cpf, data_nasc = data.split(',')

    print(f'Dados recebidos: Nome={nome}, CPF={cpf}, Data de Nascimento={data_nasc}')

    # Realiza o processamento dos dados do cliente, como salvar no banco de dados

    # Envia uma resposta ao servidor principal
    response = 'Dados recebidos e processados com sucesso!'
    conn.sendall(response.encode())
    
    conn.close() 