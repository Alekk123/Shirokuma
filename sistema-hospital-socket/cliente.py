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

        # Recebe a resposta do servidor
        response = client_socket.recv(2048).decode().strip()
        #print(response)

        # Verifica se a resposta indica que os dados são inválidos
        if 'CPF inválido ou não encontrado' in response:
            while True:
                decision = input(">")

                if decision == '1':
                    # Envia a decisão para o servidor
                    client_socket.sendall(decision.encode())
                    break
                elif decision == '2':
                    # Envia a decisão para o servidor
                    client_socket.sendall(decision.encode())
                    print("Encerrando conexão.")
                    return
                else:
                    print("Opção inválida. Por favor, escolha novamente.")
        else:
            print(response)

    # Fecha a conexão com o servidor
    # client_socket.close()

# Executa a função para inserção de dados do cliente
input_data()

"""# Criação do socket do cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#conexão com o servidor-principal
client_socket.connect((HOST, PORT))
print('Conexão estabelecida com o servidor principal.', PORT)

def inputs_client(response):
    print(response)

    if 'Escolha a opção desejada' in response:
        decision = input("Escolha uma opção: ")
        client_socket.sendall(decision.encode())
        response = client_socket.recv(2048).decode().strip()
    elif 'Bem-vindo(a), para dar continuidade aos nossos serviços por favor informe nome completo e CPF, mesmo que não tenha cadastro conosco' in response:
        nome = input("Nome completo: ")
        client_socket.sendall(nome.encode())
        cpf = input("Digite seu CPF: ")
        client_socket.sendall(cpf.encode())
     
    return response

def conect_client():
    msg_inicial = client_socket.recv(2048).decode().strip()
    response = inputs_client(msg_inicial)
    
        
    response = client_socket.recv(2048).decode().strip()
    #print(response)

    # Verifica se a resposta do servidor possui opções de escolha
    if 'Escolha a opção desejada' in response:
        # Exibe as opções de escolha para o usuário
        print(response)

        while True:
            # Recebe a escolha do usuário
            decision = input("Escolha uma opção: ")

            # Envia a escolha para o servidor principal
            client_socket.sendall(decision.encode())

            # Recebe a resposta do servidor principal
            response = client_socket.recv(2048).decode().strip()

            # Exibe a resposta do servidor
            print(response)

            # Verifica se o usuário escolheu tentar novamente ou sair
            if decision != '1' and decision != '2' and decision != '3':
                print("Opção inválida. Por favor, escolha novamente.")
            elif decision == 1:
                conect_client()
                break
            else:
                break                  
conect_client()     """       
 