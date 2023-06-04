import socket

HOST = 'localhost'  # Endereço IP do servidor principal
PORT = 5000  # Porta do servidor principal

# Criação do socket do cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conexão com o servidor principal
client_socket.connect((HOST, PORT))
print('Conexão estabelecida com o servidor principal.', PORT)

# Recebe a mensagem inicial do servidor
msg_inicial = client_socket.recv(2048).decode().strip()
print(msg_inicial)

def enviar_dados_cadastro(name, cpf):
    confirmation_msg = 'Favor confirme seu nome abaixo, está correto?\n '
    print(confirmation_msg)
    print(f'Nome = {name}\nCPF = {cpf}\n')
    while True:
        confimacao = input("Digite SIM ou NÃO para confirmar\n>").upper()
        if confimacao == 'SIM' or confimacao == 'S':
            client_socket.sendall(name.encode())
            client_socket.sendall(cpf.encode())
            break
        elif confimacao == 'NÃO' or confimacao == 'NAO' or confimacao == 'N':
            name = input ('Favor digite seu nome novamentez\n>')
            client_socket.sendall(name.encode())
            client_socket.sendall(cpf.encode())
            break
        else: 
            print("Opção inválida. Por favor, escolha novamente.")

    
    user_type = input("Digite o tipo de usuário (1 - Paciente, 2 - Médico): ")
    client_socket.sendall(user_type.encode())

    # Verifica se o tipo de usuário é médico
    if user_type == '2':
        password = input("Digite a senha: ")
        client_socket.sendall(password.encode())
        crm = input("\nDigite o CRM: ")
        client_socket.sendall(crm.encode())
        especialidade = input('Digite a especialidade: ')
        client_socket.sendall(especialidade.encode())

    # Recebe a resposta do servidor sobre o sucesso do cadastro
    response = client_socket.recv(2048).decode().strip()
    print(response)

    # Verifica se o cadastro foi realizado com sucesso
    if 'Cadastro realizado' in response:
        print("Cadastro realizado com sucesso!")
        # Continue com as operações adicionais que desejar
    else:
        print("Falha ao realizar o cadastro. Tente novamente.")

    return response
    # Fecha a conexão com o servidor
    # client_socket.close()

def input_data():   
        name = input("Nome completo: ")
        client_socket.sendall(name.encode())
        cpf = input("Digite seu CPF: ")
        client_socket.sendall(cpf.encode())

        # Recebe a resposta do servidor sobre validação dos dados
        response = client_socket.recv(2048).decode().strip()
        print(response) #ok
    
        # Verifica se a resposta indica que os dados são inválidos
        if 'CPF inválido' in response:
            while True:
                print('Escolha uma opção:\n1. Tentar novamente\n2. Sair\n')
                decision = input(">")
                if decision == '1':
                    # Envia a decisão para o servidor
                    client_socket.sendall(decision.encode())
                    input_data()
                    print('mandou os dados')
                    OK = client_socket.recv(2048).decode().strip()
                    print(OK)
                    response = client_socket.recv(2048).decode().strip()
                    print(response)

                    if 'CPF válido, porém usuário não encontrado' in response:
                        response = enviar_dados_cadastro(name, cpf)
                        print(response)
                        break
                    
                elif decision == '2':
                    # Envia a decisão para o servidor
                    client_socket.sendall(decision.encode())
                    print("Encerrando conexão.")
                    return
                else:
                    """response = client_socket.recv(1024).decode().strip()
                    print(response)
                    if 'CPF válido, porém usuário não encontrado' in response:
                        response = enviar_dados_cadastro()
                        client_socket.sendall(response.encode())"""
                    break

        # Verifica se a resposta indica que o CPF é válido
        elif 'CPF válido, porém usuário não encontrado' in response:

            #client_socket.sendall(response.encode())
            response = enviar_dados_cadastro(name, cpf)
            print(response)
            return




# Executa a função para inserção de dados do cliente
input_data()
