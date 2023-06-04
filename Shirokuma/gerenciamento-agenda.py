import socket
import json

HOST = 'localhost'
PORT = 5002

# Inicia o socket 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST, PORT))


print('Gerenciamento de Agenda iniciado e esperando por conexões.')

def consulta_date_db(date):
    with open('consultas.json', 'r') as file:
        linhas = file.readlines()

    for linha in linhas:
        dados = json.loads(linha)
        consulta_date = dados['date']
        consulta_medico_cpf = dados['medico_cpf']
        consulta_paciente_cpf = dados['paciente_cpf']

        if consulta_date == date:
            response = True 
        else: 
            response = False
            return response + consulta_medico_cpf
    return response 

def marcar_consulta(date):
    diaOcupado, cpf_medico = consulta_date_db(date)
    if diaOcupado == False:
        consulta_final = {'date': date, 'medico_cpf': cpf_medico, 'paciente_cpf': cpf}
        json_data = json.dumps(consulta_final)
        with open('consultas.json', 'a') as file:
            file.write(json_data)
            file.write('\n')
            response = "200"
    else:
        response = "406"

    return response

def show_consultas_marcadas(cpf):
    with open('consultas.json', 'r') as file:
        linhas = file.readlines()

    for linha in linhas:
        dados = json.loads(linha)
        consulta_date = dados['date']
        consulta_medico_cpf = dados['medico_cpf']
        consulta_paciente_cpf = dados['paciente_cpf']

        if consulta_medico_cpf == cpf:
            with open('user.json', 'r') as user_file:
                user_linhas = file.readlines()

                for user_linha in user_linhas:
                    user_dados = json.loads(user_linha)
                    bd_nome = user_dados["nome"]
                    bd_cpf = user_dados['cpf']
                if bd_cpf == consulta_paciente_cpf:
                    nome_paciente = bd_nome        
            print(f"Consulta no dia: {consulta_date} - Com o paciente: {nome_paciente} - de CPF: {consulta_paciente_cpf}\n")
        else: 
            print("Sem Consultas Marcadas com Você")
    return response 

while True:
    # Espera por uma conexão
    conn, addr = s.accept()
    print(f'Conectado por {addr}')

    # ...lógica do microsserviço para processar a requisição
    # Recebe os dados do servidor principal
    data = conn.recv(1024).decode().strip()

    if not data:
        # Verifica se não há mais dados a receber
        break

    # Divide os dados recebidos em nome e CPF
    name, cpf, funcao= data.split(';')

    if funcao == 1:
        dia_marcado = input("Pra que dia Gostaria de marcar sua consulta?\n (dia-mes-ano)\n>")
        marcar_consulta(dia_marcado)
    else:
        show_consultas_marcadas(cpf)


    response = consulta_date_db(cpf, funcao)
    if response: 
        response = "Consulta Realizado"
    else:
        response = "Consulta Falhou"

    conn.sendall(response.encode())

    # Fecha a conexão
    conn.close()
