import socket
import json

HOST = 'localhost'
PORT = 5002

# Inicia o socket 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST, PORT))


print('Gerenciamento de Agenda iniciado e esperando por conexões.')

while True:
    # Espera por uma conexão
    conn, addr = s.accept()
    print(f'Conectado por {addr}')

    data = conn.recv(1024).decode().strip()
    name, cpf = data.split(';')

    # Fecha a conexão
    conn.close()