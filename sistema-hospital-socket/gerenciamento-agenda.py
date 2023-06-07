import socket
import json
import random

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
    return response """

def marcar_consulta(date, cpf_cliente):
    """with open('user.json', 'r') as user_file:
        user_dados = json.load(user_file)

        medicos = user_dados['medicos']
        cpfs_medicos = [medico['cpf'] for medico in medicos]
        cpf_aleatorio = random.choice(cpfs_medicos)
        
        nome_medico = next((medico['nome'] for medico in medicos if medico['cpf'] == cpf_aleatorio), None)

        consulta_final = {'date': date, 'medico_cpf': cpf_aleatorio, 'paciente_cpf': cpf_cliente}
        json_data = json.dumps(consulta_final)
        
        response = f'Agendado Consulta para o dia {date}, com o Dr. {nome_medico}'"""
    
    
    with open('user.json', 'r') as user_file:
        user_dados = json.load(user_file)
        cpf_medicos = []
        for medico in user_dados['medicos']:
            if medico['cpf']:
                 cpf_existente = medico['cpf']
                 cpf_medicos.append(cpf_existente)
        
        cpf_consulta_medico = random.choice(cpf_medicos)  
#    diaOcupado, cpf_medico = consulta_date_db(date)
#    if diaOcupado == False:
        consulta_final = {'date': date, 'medico_cpf': cpf_consulta_medico, 'paciente_cpf': cpf}
        with open('consultas.json', 'r') as file:
            data = json.load(file)
        
        data.append(consulta_final)
    
        with open('consultas.json', 'w') as file:
            json.dump(data, file, indent=2)
        
        response = "Consulta marcada com sucesso!"
        return response
    
       
#    else:
#        response = "406"

    return response

  


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
                    #consultas.append('Sem Consultas Marcadas com Você awerjbaer')
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
        consultas.append('Sem Consultas Marcadas com Você')

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
            marcada = marcar_consulta(date, cpf)
            conn.sendall(marcada.encode())
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