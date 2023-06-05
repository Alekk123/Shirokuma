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
cadastro_dados_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cadastro_dados_sock.connect((CADASTRO_HOST, CADASTRO_PORT))

# Configurações de conexão do microserviço de agenda
GERENCIAMENTO_AGENDA_HOST = 'localhost'
GERENCIAMENTO_AGENDA_PORT = 5002
# Conecta com o microserviço de gerenciamento de agenda
gerenciamento_agenda_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
gerenciamento_agenda_sock.connect((GERENCIAMENTO_AGENDA_HOST, GERENCIAMENTO_AGENDA_PORT))


# Cria o socket do servidor principal
sock_hosp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Faz o bind do socket com o endereço e porta definidos
sock_hosp.bind((HOST, PORT))

# Define o número máximo de conexões simultâneas
sock_hosp.listen(5)
def microsservico_cadastro(name, cpf, user_type, crm=None, especialidade=None):
    print('chegou aqui bobona')
    # Verifica o tipo de usuário
    if user_type == '1':
        cadastro_dados_sock.sendall(user_type.encode())
        data = f'{name};{cpf}'
        print(name, cpf, user_type)
        cadastro_dados_sock.sendall(data.encode())
        # Retorna a resposta adequada para o cliente
        response = cadastro_dados_sock.recv(1024).decode().strip()
        return response
    elif user_type == '2':
        # Cadastro de médico
        if crm is None or especialidade is None:
            # Caso os dados adicionais (CRM e especialidade) não tenham sido fornecidos
            response = "Dados adicionais (CRM e especialidade) não foram fornecidos."
            return response
        else:
            cadastro_dados_sock.sendall(user_type.encode())
            data = f'{name};{cpf};{crm};{especialidade}'
            cadastro_dados_sock.sendall(data.encode())
            print(name, cpf, user_type, crm, especialidade)
        
        # Retorna a resposta adequada para o cliente
            response = cadastro_dados_sock.recv(1024).decode().strip()
            return response
    else:
        # Tipo de usuário inválido
        response = "Tipo de usuário inválido."
        return response

def microsservico_validador(name, cpf):
    while True:
        data = f'{name};{cpf}'
         #Envia dados para o validador
        validador_dados_sock.sendall(data.encode())
       
        #Recebe resposta do validador
        response = validador_dados_sock.recv(1024).decode().strip()

        return response

def microsservico_agenda(cpf, user_type, date=None):
    # Envia os dados da agenda para o microserviço de gerenciamento de agenda
    data = f'{cpf};{user_type};{date}'
    gerenciamento_agenda_sock.sendall(data.encode())
    
    # Recebe resposta do microserviço de gerenciamento de agenda
    response = gerenciamento_agenda_sock.recv(1024).decode().strip()
    
    return response

def receber_dados_cadastro(connection_client):
    # Recebe os dados de cadastro do cliente
    name = connection_client.recv(1024).decode().strip()
    cpf = connection_client.recv(1024).decode().strip()
    user_type = connection_client.recv(1024).decode().strip()
    print(f'{name}\n{cpf}\n{user_type}\n')
    
    if user_type == '2':
        # Recebe os dados adicionais para o cadastro de médico
        password = connection_client.recv(1024).decode().strip()
        with open('senha.txt', 'r') as file:
            senha_sistema = file.readline()
            senha_sistema = senha_sistema.rstrip('\n')
        if password == senha_sistema: 
            askCRM = ("Digite o seu CRM\n")
            connection_client.sendall(askCRM.encode())
            crm = connection_client.recv(1024).decode().strip()
            especialidade = connection_client.recv(1024).decode().strip()
            print (password, crm, especialidade)
            response = microsservico_cadastro(name, cpf, user_type, crm, especialidade)
            connection_client.sendall(response.encode())
            return response
        else:
            senhaInvalid = ("Senha incorreta")
            connection_client.sendall(senhaInvalid.encode())
    else:
        response = microsservico_cadastro(name, cpf, user_type)
        
    cliente_socket.sendall(response.encode())
    print(response)

    return response
    # Fecha a conexão com o cliente
    #connection_client.close()







# Função para lidar com a conexão do cliente
def handle_client_connection(connection_client):
    #msg_inicial de escolha
    msg_inicial = ('Bem-vindo(a), para dar continuidade aos nossos serviços por favor informe nome completo e CPF, mesmo que não tenha cadastro conosco\n')
    #envia msg pro cliente
    connection_client.sendall(msg_inicial.encode())

    # Recebe as informações do cliente
    name = connection_client.recv(1024).decode().strip()
    cpf = connection_client.recv(1024).decode().strip()
    print(f'Conexão com = {name}\nCPF = {cpf}')

    # Valide o CPF e envie a resposta para o cliente
    response = microsservico_validador(name, cpf)
    print(response)
    #connection_client.sendall(response.encode())

    if response == 'CPF inválido!':
        connection_client.sendall(response.encode())
        # Lida com a escolha do cliente
        while True:
            choice = connection_client.recv(1024).decode().strip()
            if choice == '1': # Cliente escolheu tentar novamente
                name = connection_client.recv(1024).decode().strip()
                cpf = connection_client.recv(1024).decode().strip()
                print(f'Nova conexão com {name}\nCPF = {cpf}')

                response = microsservico_validador(name, cpf)
                print(response)
                # Envia a resposta para o cliente
                connection_client.sendall(response.encode())

            elif choice == '2':
                # Cliente escolheu encerrar conexão
                break
            elif 'CPF válido, porém usuário não encontrado' in choice:
                # Inicia o processo de cadastro automaticamente
                response = receber_dados_cadastro(connection_client)
                #connection_client.sendall(response.encode())
                break
    elif response == 'CPF válido, porém usuário não encontrado. Favor realizar cadastro!':
        connection_client.sendall(response.encode())
        receber_dados_cadastro(connection_client)
    elif'CPF válido e usuário encontrado (paciente)!'in response:
        connection_client.sendall(response.encode())
        opcao = connection_client.recv(1024).decode().strip()
        print(opcao)
        if opcao == '1':
            print('sers')
        else:
            print('awjb')
        #connection_client.recv(1024).decode().strip()
    elif 'CPF válido e usuário encontrado (médico)!' in response:
        connection_client.sendall(response.encode())

        #continuação das funções do médico
        #recebe decisão do médico
    consulta = connection_client.recv(1024).decode().strip()
    print(consulta)

    
while True:
    # Espera por uma nova conexão
    cliente_socket, addr = sock_hosp.accept()
    print(f'Conexão estabelecida com {addr}')

    # Trata a conexão do cliente
    handle_client_connection(cliente_socket)



        
