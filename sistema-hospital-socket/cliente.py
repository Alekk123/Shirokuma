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
        while True:
            password = input("Digite a senha: ")
            client_socket.sendall(password.encode())
            crm_cadastro = client_socket.recv(2048).decode().strip()
            if crm_cadastro == 'Digite o seu CRM':
                print(crm_cadastro)
                crm = input(">")
                client_socket.sendall(crm.encode())
                especialidade = input('Digite a especialidade: ')
                client_socket.sendall(especialidade.encode())
                break
            else:
                print(crm_cadastro)
                
    else:
        crm = None
        especialidade = None
    # Recebe a resposta do servidor sobre o sucesso do cadastro
    response = client_socket.recv(2048).decode().strip()
    print(f'ta enxergando essa response ? {response}')

    # Verifica se o cadastro foi realizado com sucesso
    if 'Paciente cadastrado com sucesso' in response:
        response = 'Paciente cadastrado com sucesso!'
    elif 'Médico cadastrado com sucesso' in response:
        response = 'Médico cadastrado com sucesso'
    else:
        response = 'Falha ao realizar o cadastro. Tente novamente.'

    return response
    # Fecha a conexão com o servidor
    # client_socket.close()

def menu_paciente():
    while True:
        print('Bem-vindo(a) ao sistema!\nQual serviço deseja executar?\nDigite o número correspondente ao serviço desejado\n1. Agendar Consulta\n2. Verificar Consultas Agendadas\n3. Sair\n')
        opcao = input('>')

        if opcao == '1': # agendar consulta
            client_socket.sendall(opcao.encode())
            date = input("Digite a data que deseja marcar a sua consulta (dd-mm-aaaa): ")
            client_socket.sendall(date.encode())
            response = client_socket.recv(2048).decode().strip()
            print(response)
            break
        elif opcao == '2': #mostrar vericar
            client_socket.sendall(opcao.encode())
            consultas = client_socket.recv(2048).decode().strip()
            print(consultas)
            break
        elif opcao == '3':
            print('Encerrando conexão.')
            break

        else:
            print('Opção Inválida, Tente Novamente\n')

def menu_medico(name):
    print(f"Bem-vindo ao sistema, Dr. {name}\nAqui estão as suas consultas marcadas:\n")
    opcao = '2'
    client_socket.sendall(opcao.encode())
    consultas = client_socket.recv(2048).decode().strip()
    print(consultas)
            
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
                        #print('CPF válido, porém usuário não encontrado, realizando cadastro')
                        response = enviar_dados_cadastro(name, cpf)
                        print(response)

                        if 'Médico cadastrado com sucesso' in response:
                            print(response)
                            menu_medico(name)
                        elif 'Paciente cadastrado com sucesso' in response:
                            print(response)
                            menu_paciente()
                        else:
                            print('Falha ao realizar o cadastro. Tente novamente.')
                    
                elif decision == '2':
                    # Envia a decisão para o servidor
                    client_socket.sendall(decision.encode())
                    print("Encerrando conexão.")
                    return
                else:
                    break

        # Verifica se a resposta indica que o CPF é válido
        elif 'CPF válido, porém usuário não encontrado' in response:
            print('CPF válido, porém usuário não encontrado, realizando cadastro')
            #client_socket.sendall(response.encode())
            response = enviar_dados_cadastro(name, cpf)
            print(response)
            if 'Médico cadastrado com sucesso' in response:
                menu_medico(name)
            elif 'Paciente cadastrado com sucesso' in response:
                menu_paciente()
            else:
                print('Falha ao realizar o cadastro. Tente novamente.')
                return
        elif 'CPF válido e usuário encontrado (paciente)!' in response:
            print(response)
            menu_paciente()
            """print(f'Bem-vindo(a) ao sistema {name}\nQual serviço deseja executar?\nDigite o número correspondente ao serviço desejado\n1. Agendar Consulta\n2. Verificar Consultar Agendadadas\n3. Sair\n')
            while True:
                opcao = input('>')
                if opcao == '1': # agendar consulta
                    client_socket.sendall(opcao.encode())
                    date = input("Digite a data que deseja marcar a sua consulta (dd-mm-aa): ")
                    client_socket.sendall(date.encode())
                    print('Favor')
                elif opcao == '2': #mostrar vericar
                    client_socket.sendall(opcao.encode())
                    consultas = client_socket.recv(2048).decode().strip()
                    print(consultas)
                elif opcao == '3':
                    print('nada')
                    break
                else:
                    print('Opção Inválida, Tente Novamente\n')"""
                    
        elif 'CPF válido e usuário encontrado (médico)!' in response:
            print(response)
            menu_medico(name)
            """print(f"Bem vindo ao sistema Dre. {name}\n Aqui estão as suas consultas marcadas:\n")
            opcao = '2'
            client_socket.sendall(opcao.encode())
            consultas = client_socket.recv(2048).decode().strip()
            print(consultas)"""

# Executa a função para inserção de dados do cliente
input_data()
