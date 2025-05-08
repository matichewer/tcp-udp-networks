'''
Ejercicio 1: 
Diseñar un servidor de fecha y hora. El mismo deberá escuchar en el puerto 13. 
Al recibir una petición el mismo emitirá una respuesta,
devolviendo la fecha y hora del equipo donde se ejecuta y luego termina la conexión.

a) Implementar el programa utilizando el protocolo UDP.
'''

# Testeado con: echo "ping" | socat - udp:127.0.0.1:1313

from socket import *
from datetime import datetime

# Crear socket UDP
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('127.0.0.1', 1313)) 
# cambie a 1313 para evitar conflictos con el puerto 13
# con puerto 13 funciona pero hay que ejecutarlo como root

print('Servidor de fecha y hora UDP listo en el puerto 1313...')

while True:
    # Esperar mensaje
    message, clientAddress = serverSocket.recvfrom(1024)
    
    # Obtener fecha y hora actual
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Enviar respuesta
    serverSocket.sendto(now.encode(), clientAddress)
