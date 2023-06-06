import socket
import json

HOST = 'localhost'
PORT = 5002

# Inicia o socket 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST, PORT))
s.listen()

print('Gerenciamento de Agenda iniciado e esperando por conexões.')



"""def consulta_date_db(date):
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
"""
def show_consultas_marcadas(cpf, user_type):
    consultas = []

    with open('user.json', 'r') as user_file:
        user_dados = json.load(user_file)
        
    with open('consultas.json', 'r') as file:
        linhas = json.load(file)

    print(cpf, user_type)

    for dados in linhas:
        consulta_date = dados['date']
        consulta_medico_cpf = dados['medico_cpf']
        consulta_paciente_cpf = dados['paciente_cpf']
#        print(consulta_date, consulta_medico_cpf, consulta_paciente_cpf)


        if user_type == '2':
            if consulta_medico_cpf == cpf:
                    for paciente in user_dados['pacientes']:
                        if paciente['cpf'] == consulta_paciente_cpf:
                            nome_paciente = paciente['nome']
                            response = f"Consulta no dia: {consulta_date} - Com o paciente: {nome_paciente} - de CPF: {consulta_paciente_cpf}"
                            print(response)
                            consultas.append(response)
                    else:
                        consultas.append('Sem Consultas Marcadas com Você awerjbaer')
                        continue
                        
        else:
            if consulta_paciente_cpf == cpf:
                for medico in user_dados['medicos']:
                    if medico['cpf'] == consulta_medico_cpf:
                        nome_medico = medico['nome']
                        response = f"Consulta no dia: {consulta_date} - Com o medico: {nome_medico} - de CPF: {consulta_medico_cpf}\n"
                        print(response)
                        consultas.append(response)
                    else:
                        #consultas.append('Sem Consultas Marcadas com Você caruinha')
                        continue

    if not consultas:
        consultas.append('Sem Consultas Marcadas com Você nohnohno')

    return '\n'.join(consultas)
     

while True:
    # Espera por uma conexão
    conn, addr = s.accept()
    print(f'Conectado por {addr}')

    data = conn.recv(1024).decode().strip()

    if not data:
        # Verifica se não há mais dados a receber
        break

    # Divide os dados recebidos em nome e CPF
    cpf, user_type, decision_task, date = data.split(';')

    if user_type == "1":
        if decision_task == "1":
            print('nada')
            #response = marcar_consulta(date)
        else:
            consulta = show_consultas_marcadas(cpf, user_type)
            conn.sendall(consulta.encode())
    else:
        print('chegou nhon')
        consulta = show_consultas_marcadas(cpf, user_type)
        conn.sendall(consulta.encode())
    


#    response = consulta_date_db(cpf, user_type)
#    if response: 
#        response = "Consulta Realizado"
#    else:
#        response = "Consulta Falhou"

    # Fecha a conexão
    conn.close()