import socket

HOST = 'localhost'  # Endereço IP do servidor principal
PORT = 5000  # Porta do servidor principal

# Criação do socket do cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conexão com o servidor principal
client_socket.connect((HOST, PORT))
print('Conexão estabelecida com o servidor principal.', PORT)

def input_data():
    while True:
        # Recebe a mensagem inicial do servidor
        msg_inicial = client_socket.recv(2048).decode().strip()
        print(msg_inicial)

        # Verifica se a mensagem inicial contém solicitação de dados
        if 'informe nome completo e CPF' in msg_inicial:
            nome = input("Nome completo: ")
            client_socket.sendall(nome.encode())
            cpf = input("Digite seu CPF: ")
            client_socket.sendall(cpf.encode())

        # Recebe a resposta do servidor sobre validação dos dados
        response = client_socket.recv(2048).decode().strip()
        print(response)

        # Verifica se a resposta indica que os dados são inválidos
        if 'CPF inválido' in response:
            while True:
                decision = input(">")
                if decision == '1':
                    # Envia a decisão para o servidor
                    client_socket.sendall(decision.encode())
                    nome = input("Nome completo: ")
                    client_socket.sendall(nome.encode())
                    cpf = input("Digite seu CPF: ")
                    client_socket.sendall(cpf.encode())
                    response = client_socket.recv(2048).decode().strip()

                    """if decision == 'CPF válido!':
                        # Cliente validado com sucesso
                        print("Usuário validado!")
                        connection_client.sendall(validation_result.encode())
                        break"""
                    
                elif decision == '2':
                    # Envia a decisão para o servidor
                    client_socket.sendall(decision.encode())
                    break

                elif decision == '3':
                    # Envia a decisão para o servidor
                    client_socket.sendall(decision.encode())
                    print("Encerrando conexão.")
                    return
                else:
                     print("Opção inválida. Por favor, escolha novamente.")
        # Verifica se a resposta indica que o CPF é válido
        elif 'Usuário validado!' in response:
            print("Usuário validado!")
            return

    # Fecha a conexão com o servidor
    # client_socket.close()

# Executa a função para inserção de dados do cliente
input_data()

