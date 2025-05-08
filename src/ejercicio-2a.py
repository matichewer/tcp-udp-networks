'''
Ejercicio 2: Diseñar un servidor de echo. El mismo deberá recibir conexiones a través del puerto 7.
Al recibir caracteres a través de una conexión emitirá una respuesta, con los mismos caracteres
recibidos, línea por línea, sin terminar la conexión hasta que la finalice el mismo cliente.

a) Implementar el programa utilizando el protocolo TCP con la siguiente restricción: Si hay una
conexión en curso el programa no podrá recibir nuevas conexiones hasta terminar con la misma.
'''

from socket import *

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('127.0.0.1', 7777))
server_socket.listen(1)
print("Servidor de echo (TCP) escuchando en puerto 7777 (una conexión a la vez)...")

while True:
    connection_socket, addr = server_socket.accept()
    print(f"Conexión establecida con {addr}")
    
    try:
        while True:
            data = connection_socket.recv(1024)
            if not data:
                break
            connection_socket.sendall(data)
            print(f"Echo: {data.decode('utf-8').strip()}")
    except ConnectionResetError:
        print("Cliente cerró la conexión abruptamente")
    finally:
        connection_socket.close()
        print(f"Conexión con {addr} cerrada")
