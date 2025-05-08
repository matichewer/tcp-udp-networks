'''
Ejercicio 3: Diseñar un servidor de finger. El mismo deberá recibir conexiones TCP a través del
puerto 79. Al recibir una conexión el mismo emitirá una respuesta, devolviendo los datos sobre un
determinado usuario del sistema, los datos mínimos que debe informar el programa son:
    Nombre de la cuenta
    Descripción de la cuenta
    Directorio personal
    Shell asociado y fecha/hora de los último 3 ingresos
'''
'''
Execute:
    telnet 127.0.0.1 7979
Output:
    Trying 127.0.0.1...
    Connected to 127.0.0.1.
    Escape character is '^]'.
    wecher
    Login: wecher
    Nombre: Matias
    Directorio: /home/wecher
    Shell: /usr/bin/zsh
    Últimos ingresos:
    - Thu May 8 17:01:48 2025
    - screen Thu May 8 17:01:48
    - Wed May 7 10:02:21 2025
    Connection closed by foreign host.
'''


from socket import *
import threading
import pwd
import subprocess
from datetime import datetime


def handle_client(connection_socket, addr):
    try:
        print(f"Conexión establecida con {addr}")
        
        # Leer el nombre de usuario solicitado (puede venir con \r\n o \n)
        data = connection_socket.recv(1024).decode('utf-8').strip()
        username = data.split('\r\n')[0] if '\r\n' in data else data
        
        print(f"Solicitud de información para usuario: {username}")
        
        # Obtener información del usuario
        user_info = get_user_info(username) if username else None
        
        if user_info:
            response = user_info
        else:
            response = f"Usuario '{username}' no encontrado\n"
        
        # Enviar respuesta y cerrar conexión
        connection_socket.sendall(response.encode('utf-8'))
    except Exception as e:
        print(f"Error con {addr}: {str(e)}")
    finally:
        connection_socket.close()
        print(f"Conexión con {addr} cerrada")

def get_user_info(username):
    """Obtiene información real del usuario del sistema"""
    try:
        user_info = pwd.getpwnam(username)
    except KeyError:
        return None
    
    # Obtener últimos accesos REALES
    last_logins = get_real_last_logins(username)
    
    # Formatear la información del usuario
    info = f"Login: {user_info.pw_name}\n"
    info += f"Nombre: {user_info.pw_gecos}\n"
    info += f"Directorio: {user_info.pw_dir}\n"
    info += f"Shell: {user_info.pw_shell}\n"
    info += "Últimos ingresos:\n"
    for login in last_logins:
        info += f"  - {login}\n"
    
    return info

def get_real_last_logins(username):
    """Obtiene los últimos 3 accesos del usuario usando el comando 'last'"""
    try:
        result = subprocess.run(['last', '-n', '3', '-F', username], capture_output=True, text=True)
        
        if result.returncode != 0:
            return ["No se pudo obtener información de acceso"]
            
        lines = result.stdout.split('\n')
        logins = []
        
        for line in lines:
            if not line.strip() or line.startswith('wtmp begins'):
                continue
            parts = line.split()
            if len(parts) >= 6:
                # Formatear la fecha y hora
                date_str = ' '.join(parts[3:8])
                logins.append(date_str)
                if len(logins) >= 3:
                    break
        
        return logins if logins else ["No se encontraron registros de acceso"]
        
    except Exception as e:
        return [f"Error al obtener accesos: {str(e)}"]


def start_finger_server():
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 7979)) 
    server_socket.listen(5)
    print("Servidor Finger escuchando en puerto 7979...")
    
    while True:
        connection_socket, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(connection_socket, addr))
        client_thread.start()


if __name__ == "__main__":
    try:
        start_finger_server()
    except PermissionError:
        print("Error: Se necesitan privilegios de root para vincular a puerto privilegiado")
    except KeyboardInterrupt:
        print("\nServidor detenido")