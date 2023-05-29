import socket

# Configurações do servidor principal
HOST = 'localhost'
PORT = 5000

# Configurações dos microserviços
VALIDADOR_HOST = 'localhost'
VALIDADOR_PORT = 5001

GERENCIAMENTO_AGENDA_HOST = 'localhost'
GERENCIAMENTO_AGENDA_PORT = 5002

CADASTRO_HOST = 'localhost'
CADASTRO_PORT = 5003

# Cria o socket do servidor principal
sock_hosp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Faz o bind do socket com o endereço e porta definidos
sock_hosp.bind((HOST, PORT))

# Define o número máximo de conexões simultâneas
sock_hosp.listen(5)

# Conecta com o microserviço de validador de dados
validador_dados_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
validador_dados_sock.connect((VALIDADOR_HOST, VALIDADOR_PORT))

# Conecta com o microserviço de gerenciamento de agenda
"""gerenciamento_agenda_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
gerenciamento_agenda_sock.connect((GERENCIAMENTO_AGENDA_HOST, GERENCIAMENTO_AGENDA_PORT))"""

# Conecta com o microserviço de cadastro de pacientes
"""cadastro_pacientes_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cadastro_pacientes_sock.connect((CADASTRO_HOST, CADASTRO_PORT))"""

# Função para lidar com a conexão do cliente
def handle_client(connection_client):
    while True:
        #msg_inicial de escolha
        msg_inicial = ('Bem-vindo(a), para dar continuidade aos nossos serviços por favor informe nome completo e CPF, mesmo que não tenha cadastro conosco\n')
        #envia msg pro cliente
        connection_client.sendall(msg_inicial.encode())
        # Recebe as informações do cliente
        name = connection_client.recv(1024).decode().strip()
        print(name)
        cpf = connection_client.recv(1024).decode().strip()
        print(f'Conexão com = {name}\nCPF = {cpf}')

        #while True:
        # Enviar os dados para o microsserviço de validação de dados
        validador_dados_sock.sendall(name.encode())
        validador_dados_sock.sendall(cpf.encode())

        # Recebe a resposta do servidor de validação
        validador_response = validador_dados_sock.recv(1024).decode().strip()
        validador_dados_sock.close()
        #connection_client.sendall(validador_response.encode())

        # Resposta para o cliente
        if validador_response == 'CPF válido!':
            response = f'Usuário validado!, Bem-vindo(a) {name}'
            connection_client.sendall(response.encode())
        else:
            response = '\nCPF inválido ou não encontrado\n==Escolha a opção desejada==\n1. Tentar Novamente\n2. Realizar Cadastro\n3. Sair'
            connection_client.sendall(response.encode())
        
            while True:
                # Recebe a escolha do cliente
                decision = connection_client.recv(1024).decode().strip()

                # Verifica a escolha do cliente
                if decision == '1':
                    # Continua o loop e permite que o cliente tente novamente
                    handle_client(connection_client)
                    #connection_client.sendall(response.encode())
                    continue
                elif decision == '2':
                    # Encerra o loop e finaliza a conexão com o cliente
                    response = 'Encerrando conexão'
                    connection_client.sendall(response.encode())
                    return   


while True:
    # Espera por uma nova conexão
    cliente_socket, addr = sock_hosp.accept()
    print(f'Conexão estabelecida com {addr}')

    # Trata a conexão do cliente
    handle_client(cliente_socket)



        
