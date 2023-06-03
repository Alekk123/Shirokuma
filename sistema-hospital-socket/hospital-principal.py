import socket

# Configurações do servidor principal
HOST = 'localhost'
PORT = 5000

#Configurações conexão com o microsserviço de validação
VALIDADOR_HOST = 'localhost'
VALIDADOR_PORT = 5001
# Criação do socket 
validador_dados_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Conecta com o microserviço de validador de dados
validador_dados_sock.connect((VALIDADOR_HOST, VALIDADOR_PORT))

# Configurações conexão com o microsserviço de cadastro
CADASTRO_HOST = 'localhost'
CADASTRO_PORT = 5003
# Criação do socket cadastro
"""cadastro_dados_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cadastro_dados_sock.connect((CADASTRO_HOST, CADASTRO_PORT))"""

# Configurações de conexão do microserviço de agenda
GERENCIAMENTO_AGENDA_HOST = 'localhost'
GERENCIAMENTO_AGENDA_PORT = 5002
# Conecta com o microserviço de gerenciamento de agenda
"""gerenciamento_agenda_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
gerenciamento_agenda_sock.connect((GERENCIAMENTO_AGENDA_HOST, GERENCIAMENTO_AGENDA_PORT))"""


# Cria o socket do servidor principal
sock_hosp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Faz o bind do socket com o endereço e porta definidos
sock_hosp.bind((HOST, PORT))

# Define o número máximo de conexões simultâneas
sock_hosp.listen(5)


def microsservico_validador(name, cpf):
    while True:
        data = f'{name};{cpf}'
         #Envia dados para o validador
        validador_dados_sock.sendall(data.encode())
       
        #Recebe resposta do validador
        response = validador_dados_sock.recv(1024).decode().strip()

        # Fecha a conexão com o microsserviço de validação
        #validador_dados_sock.close()

        return response

"""def microservico_cadastro(name, cpf, tipo):

    response  = ca
    return response
"""
"""def microsservico_gerenciamento():
    return"""


# Função para lidar com a conexão do cliente
def connection_client(connection_client):
    #msg_inicial de escolha
    msg_inicial = ('Bem-vindo(a), para dar continuidade aos nossos serviços por favor informe nome completo e CPF, mesmo que não tenha cadastro conosco\n')
    #envia msg pro cliente
    connection_client.sendall(msg_inicial.encode())
    # Recebe as informações do cliente
    name = connection_client.recv(1024).decode().strip()
    print(name)
    cpf = connection_client.recv(1024).decode().strip()
    print(f'Conexão com = {name}\nCPF = {cpf}')

    # Valide o CPF e envie a resposta para o cliente
    response = microsservico_validador(name, cpf)
    connection_client.sendall(response.encode())


    # Lida com a escolha do cliente
    while True:
        choice = connection_client.recv(1024).decode().strip()
        if choice == '1': # Cliente escolheu tentar novamente
            name = connection_client.recv(1024).decode().strip()
            cpf = connection_client.recv(1024).decode().strip()
            print(f'Nova conexão com {name}\nCPF = {cpf}')
            response = microsservico_validador(name, cpf)
            
            #response = validador_dados_sock.recv(1024).decode().strip()
            print(response)

            # Envia a resposta para o cliente
            connection_client.sendall(response.encode())
        elif choice == '2':
            # Cliente escolheu encerrar conexão
            break
        else:
            # Opção inválida
            invalid_option = "Opção inválida. Por favor, escolha novamente."

            # Verifica se o CPF é válido, mas não encontrado
            if 'CPF válido, porém usuário não encontrado' in response:
                # Inicia o processo de cadastro automaticamente
                response = receber_dados_cadastro(connection_client)
                connection_client.sendall(response.encode())
                break

def receber_dados_cadastro(connection_client):
    # Envia uma mensagem de confirmação para o cliente
    confirmation_msg = "Envie os dados de cadastro."
    #connection_client.sendall(confirmation_msg.encode())

    # Recebe os dados de cadastro do cliente
    name = connection_client.recv(1024).decode().strip()
    cpf = connection_client.recv(1024).decode().strip()
    user_type = connection_client.recv(1024).decode().strip()
    print(f'{name}\n, {cpf}\n{user_type}\n')

    # Processa os dados de cadastro
    """response = microservico_cadastro(name, cpf, user_type)
    connection_client.sendall(response.encode())"""

    # Fecha a conexão com o cliente
    #connection_client.close()

while True:
    # Espera por uma nova conexão
    cliente_socket, addr = sock_hosp.accept()
    print(f'Conexão estabelecida com {addr}')

    # Trata a conexão do cliente
    connection_client(cliente_socket)



        
