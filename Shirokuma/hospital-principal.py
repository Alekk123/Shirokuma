import socket
import json

# Configurações do servidor principal
HOST = 'localhost'
PORT = 5000

# Configurações dos microserviços
GERENCIAMENTO_AGENDA_HOST = 'localhost'
GERENCIAMENTO_AGENDA_PORT = 5002

CADASTRO_HOST = 'localhost'
CADASTRO_PORT = 5003

# Configurações conexão com o microsserviço de validação
VALIDADOR_HOST = 'localhost'
VALIDADOR_PORT = 5001
# Criação do socket validador
validador_dados_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Conecta com o microserviço de validador de dados
validador_dados_sock.connect((VALIDADOR_HOST, VALIDADOR_PORT))

# Criação do socket cadastro
cadastro_dados_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cadastro_dados_sock.connect((CADASTRO_HOST, CADASTRO_PORT))


# Cria o socket do servidor principal
sock_hosp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Faz o bind do socket com o endereço e porta definidos
sock_hosp.bind((HOST, PORT))

# Define o número máximo de conexões simultâneas
sock_hosp.listen(5)


# Conecta com o microserviço de gerenciamento de agenda
"""gerenciamento_agenda_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
gerenciamento_agenda_sock.connect((GERENCIAMENTO_AGENDA_HOST, GERENCIAMENTO_AGENDA_PORT))"""

# Conecta com o microserviço de cadastro de pacientes
"""cadastro_pacientes_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cadastro_pacientes_sock.connect((CADASTRO_HOST, CADASTRO_PORT))"""


def microsservico_validador(name, cpf):
    while True:
        data = f'{name};{cpf}'
        validador_dados_sock.sendall(data.encode())
        # Envia dados para o validador
        # validador_dados_sock.sendall(name.encode())
        # validador_dados_sock.sendall(cpf.encode())
        # Recebe resposta do validador
        response = validador_dados_sock.recv(1024).decode().strip()

        # Fecha a conexão com o microsserviço de validação
        # validador_dados_sock.close()

        return response


def microsservico_cadastro(name, cpf, funcao, crm):
    while True:
        data = f'{name};{cpf};{funcao};{crm}'
        cadastro_dados_sock.sendall(data.encode())
        response_cadastro = cadastro_dados_sock.recv(1024).decode().strip()
        return response_cadastro
    
def consulta_db(cpf):
    with open('user.json', 'r') as file:
        linhas = file.readlines()

    for linha in linhas:
        dados = json.loads(linha)
#        bd_nome = dados['nome']
        bd_cpf = dados['cpf']
#        bd_funcao = dados['funcao']
#        bd_crm = dados.get('crm', None)

        if bd_cpf == cpf:
            response = True
            return response
    response = False
    return response

"""def microsservico_gerenciamento():
    return
def microservico_cadastro():
    return"""

# Função para lidar com a conexão do cliente


def connection_client(connection_client):
    # msg_inicial de escolha
    msg_inicial = (
        'Bem-vindo(a), para dar continuidade aos nossos serviços por favor informe nome completo e CPF, mesmo que não tenha cadastro conosco\n')
    # envia msg pro cliente
    connection_client.sendall(msg_inicial.encode())
    # Recebe as informações do cliente
    name = connection_client.recv(1024).decode().strip()
    print(name)
    cpf = connection_client.recv(1024).decode().strip()
    print(f'Conexão com = {name}\nCPF = {cpf}')

    # Valide o CPF e envie a resposta para o cliente
    if microsservico_validador(name, cpf) == 'CPF válido!':
        response = 'CPF válido!'
        connection_client.sendall(response.encode())
    else:
        response = 'CPF inválido!'
        connection_client.sendall(response.encode())

    # connection_client.sendall(response.encode())

    # Lida com a escolha do cliente
    while True:
        choice = connection_client.recv(1024).decode().strip()
        if choice == '1':  # Cliente escolheu tentar novamente
            name = connection_client.recv(1024).decode().strip()
            cpf = connection_client.recv(1024).decode().strip()
            print(f'Nova conexão com {name}\nCPF = {cpf}')
            response = microsservico_validador(name, cpf)

            # response = validador_dados_sock.recv(1024).decode().strip()
            print(response)

            # Envia a resposta para o cliente
            connection_client.sendall(response.encode())

            # Valide o novo CPF e envie a resposta para o cliente
            """if microsservico_validador(name, cpf):
                response = 'CPF válido!'
            else:
                response = 'CPF inválido!'

            connection_client.sendall(response.encode())"""

        elif choice == '2':
            # Cliente escolheu realizar cadastro
            name = connection_client.recv(1024).decode().strip()
            cpf = connection_client.recv(1024).decode().strip()
            #connection_client.sendall(response.encode())
            if microsservico_validador(name, cpf) == 'CPF válido!':
                isCPFinDB = consulta_db(cpf)
                if isCPFinDB == True:
                    #microsservico_gerenciamento()
                    break
                elif isCPFinDB == False:
                    funcCadastroMSG = ("Selecione sua Funcao\n1 - Paciente\n2 - Medico\n")
                    connection_client.sendall(funcCadastroMSG.encode())
                    funcao = connection_client.recv(1024).decode().strip()
                    if funcao == 1:                            
                        microsservico_cadastro(name, cpf, funcao, crm)
                        #microsservico_gerenciamento()
                        break
                    elif funcao == 2:
                        askSenha = ("Digite a Senha para Cadastro:\n")
                        connection_client.sendall(askSenha.encode())
                        senha_cadastro = connection_client.recv(1024).decode().strip()
                        with open('senha.txt', 'r') as file:
                            senha_sistema = file.readline()
                            senha_sistema = senha_sistema.rstrip('\n')
                        if senha_cadastro == senha_sistema: 
                            askCRM = ("Digite o seu CRM:\n")
                            connection_client.sendall(askCRM.encode())
                            crm = connection_client.recv(1024).decode().strip()    
                            microsservico_cadastro(name, cpf, funcao, crm)
                    else:
                        response = 'CPF inválido!'
                        return response
            # Outras ações relacionadas ao cadastro
#            break
        elif choice == '3':
            # Cliente escolheu encerrar conexão
            break
        else:
            # Opção inválida
            invalid_option = "Opção inválida. Por favor, escolha novamente."


# def start_server():

while True:
    # Espera por uma nova conexão
    cliente_socket, addr = sock_hosp.accept()
    print(f'Conexão estabelecida com {addr}')

    # Trata a conexão do cliente
    connection_client(cliente_socket)
