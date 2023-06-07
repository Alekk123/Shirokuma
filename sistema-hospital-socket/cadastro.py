import socket
import json

HOST = 'localhost'
PORT = 5003

# Inicia o socket 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST, PORT))
s.listen()


print('Cadastro iniciado e esperando por conexões.')

with open('user.json', 'r') as file:
    data = json.load(file)

while True:
    # Espera por uma conexão
    conn, addr = s.accept()
    print(f'Conectado por {addr}')

    # Recebe os dados do cliente
    print('recebendo')

    user_type = conn.recv(1024).decode().strip()
    if user_type == '1':
        client_data = conn.recv(1024).decode().strip()
        name, cpf = client_data.split(';')
        print(f'Dados recebidos: Nome = {name}, CPF = {cpf}, tipo = {user_type}')
        response = 'Paciente cadastrado com sucesso'
        conn.sendall(response.encode())

        data['pacientes'].append({
            'nome': name,
            'cpf': cpf,
            'funcao': int(user_type),
        })
 

    elif user_type == '2':
        client_data = conn.recv(1024).decode().strip()
        name, cpf, crm, especialidade = client_data.split(';')
        print(f'Dados recebidos: Nome = {name}, CPF = {cpf}, tipo = {user_type}, crm = {crm}, especialidade = {especialidade}')
        response = 'Médico cadastrado com sucesso'
        conn.sendall(response.encode())
        data['medicos'].append({
            'nome': name,
            'cpf': cpf,
            'funcao': int(user_type),
            'crm': crm,
            'especialidade': especialidade
        })
    elif user_type == 'GET_LISTA_MEDICOS':
        lista_medicos = data['medicos']
        lista_medicos_json = json.dumps(lista_medicos)
        conn.sendall(lista_medicos_json.encode())
        
    #conn.sendall(response.encode())

    with open('user.json', 'w') as file:
        json.dump(data, file, indent=2)
    
    #conn.close() 