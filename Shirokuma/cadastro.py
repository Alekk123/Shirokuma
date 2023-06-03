import socket
import json

HOST = 'localhost'
PORT = 5003

# Inicia o socket 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST, PORT))
s.listen()


print('Cadastro iniciado e esperando por conexoes.')

def cadastro(name, cpf):
    
    while True:
        if funcao == '1':          
            cliente_final = {'nome': name, 'cpf': cpf, 'funcao': 1, 'crm': ' '}
            json_data = json.dumps(cliente_final)
            with open('user.json', 'a') as file:
                file.write(json_data)
                file.write('\n')
            return True
            """ json_data = json.loads(cliente_final('utf-8'))
            with open('user.json', 'a') as file:
               json.dumps(json_data , file )                file.write('\n')"""
        elif funcao == '2':    
            cliente_final = {'nome': name, 'cpf': cpf, 'funcao': 2, 'crm': crm}
            json_data = json.dumps(cliente_final)
            with open('user.json', 'a') as file:
                file.write(json_data)
                file.write('\n')
#               json_data = json.loads(cliente_final('utf-8'))
#                with open('user.json', 'a') as file:
#                    json.dumps(json_data , file )
#                    file.write('\n')
            return True   
        else:
            print("Opção inválida. Por favor, escolha novamente.")
            return False

while True:
    # Espera por uma conexao
    conn, addr = s.accept()
    print(f'Conectado por {addr}')

    while True:
        # Recebe os dados do servidor principal
        data = conn.recv(1024).decode().strip()

        if not data:
            # Verifica se não há mais dados a receber
            break

        # Divide os dados recebidos em nome e CPF
        name, cpf, funcao, crm = data.split(';')


        response = cadastro(name, cpf, funcao, crm)
        if response: 
            response = "Cadastro Realizado"
        else:
            response = "Cadastro Falhou"

        conn.sendall(response.encode())


    # Recebe os dados do cliente
    """data = conn.recv(1024).decode().strip()
    print('recebendo')
    nome, cpf, data_nasc = data.split(',')

    print(f'Dados recebidos: Nome={nome}, CPF={cpf}, Data de Nascimento={data_nasc}')

    # Realiza o processamento dos dados do cliente, como salvar no banco de dados

    # Envia uma resposta ao servidor principal
    response = 'Dados recebidos e processados com sucesso!'
    conn.sendall(response.encode())
    """
    #conn.close() 
