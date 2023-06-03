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


                    if decision == 'CPF válido!':
                        # Cliente validado com sucesso
                        print("Usuário validado!")
                        #client_socket.sendall(validation_result.encode())
                        break
                    
                elif decision == '2':
                    # Envia a decisão para o servidor
                    client_socket.sendall(decision.encode())
                    print("Encerrando conexão.")
                    return
                else:
                     print("Opção inválida. Por favor, escolha novamente.")

        # Verifica se a resposta indica que o CPF é válido
        elif 'CPF válido, porém usuário não encontrado' in response:
            #print("CPF válido, porém usuário não encontrado. Favor realizar cadastro!")
            response = enviar_dados_cadastro(name, cpf, client_socket)
            print(response)
            return


def enviar_dados_cadastro(name, cpf, client_socket):
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

    while True:
        user_type = input("Digite o tipo de usuário (1 - Paciente, 2 - Médico): ")
        if user_type in ['1', '2']:
            break
        else:
            print("Opção inválida. Por favor, escolha novamente.")

        client_socket.sendall(user_type.encode())

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

# Executa a função para inserção de dados do cliente
input_data()
