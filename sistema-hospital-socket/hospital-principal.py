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
"""validador_dados_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
validador_dados_sock.connect((VALIDADOR_HOST, VALIDADOR_PORT))"""

# Conecta com o microserviço de gerenciamento de agenda
"""gerenciamento_agenda_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
gerenciamento_agenda_sock.connect((GERENCIAMENTO_AGENDA_HOST, GERENCIAMENTO_AGENDA_PORT))"""

# Conecta com o microserviço de cadastro de pacientes
cadastro_pacientes_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cadastro_pacientes_sock.connect((CADASTRO_HOST, CADASTRO_PORT))

# Função para lidar com a conexão do cliente
def handle_client(connection):
    #menu de escolha
    menu = ('Bem-vindo(a) para dar continuidade ao atendimento, por favor escolha uma das seguintes opções (selecione apenas o número)\n1. Primeiro Acesso Paciente\n2. Primeiro Acesso Médico\n3. Login\n')
    #envia msg pro cliente
    connection.sendall(menu.encode())
    # Recebe a escolha do cliente
    choice = connection.recv(1024).decode().strip()

    if choice == 1:
        # Primeiro acesso - solicita os dados do cliente
        connection.sendall('Digite seu nome completo: '.encode())
        nome = connection.recv(1024).decode().strip()
        connection.sendall('Digite seu nome CPF: '.encode())
        cpf = connection.recv(1024).decode().strip()
        connection.sendall('Digite sua data de nascimento (DD/MM/AAAA): '.encode())
        data_nasc = connection.recv(1024).decode().strip()

        # Conecta ao servidor de cadastro e envia os dados
        cadastro_data = f'{nome},{cpf},{data_nasc}'
        cadastro_pacientes_sock.sendall(cadastro_data.encode())

        # Recebe a resposta do servidor de cadastro
        cadastro_response = cadastro_pacientes_sock.recv(1024).decode().strip()
        connection.sendall(cadastro_response.encode())
        
        # Exemplo de resposta para o cliente
        response = 'Servidor principal: Conexão recebida com sucesso!'
        connection.sendall(response.encode())

        # Fechar a conexão com o cliente
        #connection.close()

while True:
    # Espera por uma nova conexão
    cliente_socket, addr = sock_hosp.accept()
    print(f'Conexão estabelecida com {addr}')

    # Trata a conexão do cliente
    handle_client(cliente_socket)



        
