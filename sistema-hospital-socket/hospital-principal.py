import socket

# Configurações do servidor principal
HOST = 'localhost'
PORT = 5000

# Configurações dos microserviços
GERENCIAMENTO_AGENDA_HOST = 'localhost'
GERENCIAMENTO_AGENDA_PORT = 5002

CADASTRO_HOST = 'localhost'
CADASTRO_PORT = 5003

#Configurações conexão com o microsserviço de validação
VALIDADOR_HOST = 'localhost'
VALIDADOR_PORT = 5001
# Criação do socket 
validador_dados_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Conecta com o microserviço de validador de dados
validador_dados_sock.connect((VALIDADOR_HOST, VALIDADOR_PORT))

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
        #Envia dados para o validador
        #validador_dados_sock.sendall(name.encode())
        #validador_dados_sock.sendall(cpf.encode())
        #Recebe resposta do validador
        response = validador_dados_sock.recv(1024).decode().strip()

        # Fecha a conexão com o microsserviço de validação
        #validador_dados_sock.close()

        return response


"""def microsservico_gerenciamento():
    return
def microservico_cadastro():
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
    if microsservico_validador(name, cpf) == 'CPF válido!':
        response = 'CPF válido!'
    else:
        response = 'CPF inválido!'

    connection_client.sendall(response.encode())

    # Lida com a escolha do cliente
    while True:
        choice = connection_client.recv(1024).decode().strip()
        if choice == '1':
            # Cliente escolheu tentar novamente
            connection_client.sendall('OK'.encode())
            name = connection_client.recv(1024).decode().strip()
            cpf = connection_client.recv(1024).decode().strip()
            print(f'Nova conexão com {name}\nCPF = {cpf}')
            response = microsservico_validador(name, cpf)
            #validador_dados_sock.sendall(name.encode())
            #validador_dados_sock.sendall(cpf.encode())
            
            #response = validador_dados_sock.recv(1024).decode().strip()
            print(response)

            # Envia a resposta para o cliente
            connection_client.sendall(response.encode())

            # Valide o novo CPF e envie a resposta para o cliente
            if microsservico_validador(name, cpf):
                response = 'CPF válido!'
            else:
                response = 'CPF inválido!'

            connection_client.sendall(response.encode())
            
        elif choice == '2':
            # Cliente escolheu realizar cadastro
            connection_client.sendall('OK'.encode())
            # Outras ações relacionadas ao cadastro
            break
        elif choice == '3':
            # Cliente escolheu encerrar conexão
            break
        else:
            # Opção inválida
            invalid_option = "Opção inválida. Por favor, escolha novamente."

    """validation_result = microsservico_validador(name, cpf)

    #CPF valido
    if validation_result == 'CPF válido!':
        # Cliente validado com sucesso
        print("Usuário validado!")
        connection_client.sendall(validation_result.encode())
    else: #CPF Invalido
        while True:
            # Envia opções para o cliente escolher
            invalid_message = "CPF inválido. Escolha uma opção:\n1. Tentar novamente\n2. Realizar cadastro\n3. Sair\n"
            connection_client.sendall(invalid_message.encode())
            #Recebe escolha o usuário
            choice = connection_client.recv(1024).decode().strip()
            if choice == '1':
                name = connection_client.recv(1024).decode().strip()
                print(name)
                cpf = connection_client.recv(1024).decode().strip()
                print(f'CPF do loop = {cpf}')
                validation = microsservico_validador(name, cpf)
                print('mandou??')
                print(validation)

                if validation == 'CPF válido!':
                    # Cliente validado com sucesso
                    print("Usuário validado!")
                    connection_client.sendall(validation_result.encode())
                    break
                else:
                    print('Invalidoo')
            elif choice == '2':
                # Cliente escolheu realizar cadastro
                print("Cliente escolheu realizar cadastro.")
                # Outras ações relacionadas ao cadastro
                break  # Encerra o loop e fecha a conexão com o cliente
            elif choice == '3':
                # Cliente escolheu encerrar conexão
                break
            else:
                # Opção inválida
                invalid_option = "Opção inválida. Por favor, escolha novamente."
                connection_client.sendall(invalid_option.encode())
       
    """
#def start_server():

while True:
    # Espera por uma nova conexão
    cliente_socket, addr = sock_hosp.accept()
    print(f'Conexão estabelecida com {addr}')

    # Trata a conexão do cliente
    connection_client(cliente_socket)



        
