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
#        print(response) #ok
    
        # Verifica se a resposta indica que os dados são inválidos
        if 'CPF inválido' in response:
            while True:
                print('Escolha uma opção:\n1. Tentar novamente\n2. Realizar cadastro\n3. Sair\n')
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

                            
                    """client_socket.sendall(decision.encode())
                    nome = input("Nome completo: ")
                    client_socket.sendall(nome.encode())
                    cpf = input("Digite seu CPF: ")
                    client_socket.sendall(cpf.encode())
                    response = client_socket.recv(2048).decode().strip()
                    print(response)"""

                    if decision == 'CPF válido!':
                        # Cliente validado com sucesso
                        print("Usuário validado!")
                        #client_socket.sendall(validation_result.encode())
                        break
                    
                elif decision == '2':
                    # Envia a decisão para o servidor
                    client_socket.sendall(decision.encode())
#                    response = client_socket.recv(2048).decode().strip()
                    choose_function = client_socket.recv(2048).decode().strip()
                    print(choose_function)
                    funcao = input("Funcao: ")
                    client_socket.sendall(funcao.encode())
                    cadastro_senha = client_socket.recv(2048).decode().strip()
                    print(cadastro_senha)
                    senha_cadastro = input("Senha: ")
                    client_socket.sendall(senha_cadastro.encode())
                    crm_cadastro = client_socket.recv(2048).decode().strip()
                    print(crm_cadastro)
                    crm = input("CRM: ")
                    client_socket.sendall(crm.encode())
                    response = client_socket.recv(2048).decode().strip()
                    print('mandou os dados')
                    OK = client_socket.recv(2048).decode().strip()
                    print(OK)
                    response = client_socket.recv(2048).decode().strip()
                    print(response)
                    #break

                elif decision == '3':
                    # Envia a decisão para o servidor
                    client_socket.sendall(decision.encode())
                    print("Encerrando conexão.")
                    return
                else:
                     print("Opção inválida. Por favor, escolha novamente.")
                return decision
        # Verifica se a resposta indica que o CPF é válido
        elif 'CPF válido!' in response:
            print("Usuário validado!")
            return

    # Fecha a conexão com o servidor
        client_socket.close()

# Executa a função para inserção de dados do cliente
input_data()

