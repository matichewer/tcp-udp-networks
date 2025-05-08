'''
Ejercicio 1: 
Diseñar un servidor de fecha y hora. El mismo deberá escuchar en el puerto 13. 
Al recibir una petición el mismo emitirá una respuesta,
devolviendo la fecha y hora del equipo donde se ejecuta y luego termina la conexión.

b) Implementar el programa utilizando el protocolo TCP con la siguiente restricción: Si hay una
conexión en curso el programa no podrá recibir nuevas conexiones hasta terminar con la misma.
'''

# Para testear: telnet 127.0.0.1 1313

from socket import *
from datetime import datetime

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('127.0.0.1', 1313))
serverSocket.listen(1)  # Solo una conexión pendiente

print('Servidor de fecha y hora TCP listo en el puerto 1313...')

try:
    while True:
        connectionSocket, clientAddress = serverSocket.accept()
        
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        connectionSocket.send(now.encode())
        
        connectionSocket.close()
except KeyboardInterrupt:
    print("\nCerrando servidor...")
    serverSocket.close()  # Cierra el socket correctamente