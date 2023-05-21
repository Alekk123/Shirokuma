import socket

# Configurações do servidor principal
HOST = 'localhost'
PORT = 5000

# Configurações dos microserviços
VALIDADOR_DADOS_HOST = 'localhost'
VALIDADOR_DADOS_PORT = 5001

GERENCIAMENTO_AGENDA_HOST = 'localhost'
GERENCIAMENTO_AGENDA_PORT = 5002

CADASTRO_PACIENTES_HOST = 'localhost'
CADASTRO_PACIENTES_PORT = 5003

# Cria o socket do servidor principal
sock_hosp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Faz o bind do socket com o endereço e porta definidos
sock_hosp.bind((HOST, PORT))

# Define o número máximo de conexões simultâneas
sock_hosp.listen(5)

# Conecta com o microserviço de validador de dados
validador_dados_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
validador_dados_sock.connect((VALIDADOR_DADOS_HOST, VALIDADOR_DADOS_PORT))

# Conecta com o microserviço de gerenciamento de agenda
gerenciamento_agenda_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
gerenciamento_agenda_sock.connect((GERENCIAMENTO_AGENDA_HOST, GERENCIAMENTO_AGENDA_PORT))

# Conecta com o microserviço de cadastro de pacientes
cadastro_pacientes_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cadastro_pacientes_sock.connect((CADASTRO_PACIENTES_HOST, CADASTRO_PACIENTES_PORT))

"""with sock_hosp as s:
    # Liga o socket à porta e ao IP do servidor
    s.bind((HOST, PORT))
    # Coloca o socket em modo de escuta
    s.listen()
    print(f'Servidor principal iniciado. Aguardando conexões na porta {PORT}...')
    while True:
        # Espera por uma conexão
        conn, addr = s.accept()
        print(f'Conexão estabelecida com {addr}')"""
        





while True:
    # Espera por uma nova conexão
    cliente_socket, addr = sock_hosp.accept()
    print(f'Conexão estabelecida com {addr}')