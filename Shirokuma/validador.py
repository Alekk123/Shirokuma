import socket
import json

HOST = 'localhost'
PORT = 5001

# Inicia o socket 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST, PORT))
s.listen()


print('Microsserviço iniciado e esperando por conexões.')

def valida_cpf(cpf):
    # Remove caracteres não numéricos do CPF
    cpf = ''.join(filter(str.isdigit, cpf))

    # Verifica se o CPF possui 11 dígitos
    if len(cpf) != 11:
        return False

    # Verifica se todos os dígitos são iguais
    if cpf == cpf[0] * 11:
        return False

    # Calcula o primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto

    # Verifica o primeiro dígito verificador
    if int(cpf[9]) != digito1:
        return False

    # Calcula o segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto

    # Verifica o segundo dígito verificador
    if int(cpf[10]) != digito2:
        return False

    return True

while True:
    # Espera por uma conexão
    conn, addr = s.accept()
    print(f'Conectado por {addr}')
    
    while True:
        # Recebe os dados do servidor principal
        data = conn.recv(1024).decode().strip()

        if not data:
            # Verifica se não há mais dados a receber
            break

        # Divide os dados recebidos em nome e CPF
        name, cpf = data.split(';')

        print(f'Recebido dados de {name}\nCPF = {cpf}')

        # Valida o CPF
        if valida_cpf(cpf):
            response = 'CPF válido!'
        else:
            response = 'CPF inválido!'

        # Envia a resposta de volta para o servidor principal
        conn.sendall(response.encode())
# Fecha a conexão
#conn.close()