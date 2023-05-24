import socket

HOST = 'localhost'
PORT = 5001

# Inicia o socket 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST, PORT))
s.listen()


print('Microsserviço iniciado e esperando por conexões.')

while True:
    # Espera por uma conexão
    conn, addr = s.accept()
    print(f'Conectado por {addr}')

    # ...lógica do microsserviço para processar a requisição
 
    # Fecha a conexão
    conn.close()