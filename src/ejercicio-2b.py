'''
Ejercicio 2: Diseñar un servidor de echo. El mismo deberá recibir conexiones a través del puerto 7.
Al recibir caracteres a través de una conexión emitirá una respuesta, con los mismos caracteres
recibidos, línea por línea, sin terminar la conexión hasta que la finalice el mismo cliente.

b) Implementar el programa utilizando el protocolo TCP. El programa deberá poder recibir más de
una conexión al mismo sobre el puerto de escucha.
'''

from socket import *
import threading

def handle_client(connection_socket, addr):
    try:
        print(f"Conexión establecida con {addr}")
        while True:
            data = connection_socket.recv(1024)
            if not data:
                break
            connection_socket.sendall(data)
            print(f"Echo a {addr}: {data.decode('utf-8').strip()}")
    except ConnectionResetError:
        print(f"Cliente {addr} cerró la conexión abruptamente")
    finally:
        connection_socket.close()
        print(f"Conexión con {addr} cerrada")


server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('127.0.0.1', 7777))
server_socket.listen(5)
print("Servidor de echo (TCP) escuchando en puerto 7 (múltiples conexiones)...")

while True:
    connection_socket, addr = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(connection_socket, addr))
    client_thread.start()

