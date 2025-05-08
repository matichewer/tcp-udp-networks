'''
Ejercicio 1: 
Diseñar un servidor de fecha y hora. El mismo deberá escuchar en el puerto 13. 
Al recibir una petición el mismo emitirá una respuesta,
devolviendo la fecha y hora del equipo donde se ejecuta y luego termina la conexión.

c) Implementar el programa utilizando el protocolo TCP con la siguiente restricción: 
Si hay una conexión en curso el programa no podrá recibir nuevas conexiones hasta terminar con la misma.
'''

# Para testear: telnet 127.0.0.1 1313


from socket import *
from datetime import datetime
import threading

def manejar_cliente(connectionSocket, clientAddress):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    connectionSocket.send(now.encode())
    connectionSocket.close()

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('127.0.0.1', 1313))
serverSocket.listen(5)  # Permite hasta 5 conexiones pendientes

print('Servidor de fecha y hora TCP listo en el puerto 1313...')

try:
    while True:
        connectionSocket, clientAddress = serverSocket.accept()
        hilo = threading.Thread(target=manejar_cliente, args=(connectionSocket, clientAddress))
        hilo.start()
except KeyboardInterrupt:
    print("\nCerrando servidor...")
    serverSocket.close()  # Cierra el socket correctamente
