# importar librerias necesarias
import socket
import threading

# El cliente elige un apodo
apodo = input("Indique un nombre para ingresar a la sala: ")

# Conectarse al servidor
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(('127.0.0.1', 55555))

# Escuchar al servidor y enviar apodo
def recibir():
    while True:
        try:
            # Recibir mensajes del servidor
            mensaje = cliente.recv(1024).decode('ascii')
            if mensaje == 'NICK':
                cliente.send(apodo.encode('ascii'))
            else:
                print(mensaje)
        except:
            # Cerrar la conexion cuando hay error
            print("Ha ocurrido un error!")
            cliente.close()
            break

# Enviar mensajes al servidor
def escribir():
    while True:
        mensaje = '{}: {}'.format(apodo, input(''))
        cliente.send(mensaje.encode('ascii'))

# Iniciar proceso de conversación. Escuchar y escribir
recibir_thread = threading.Thread(target=recibir)
recibir_thread.start()

escribir_thread = threading.Thread(target=escribir)
escribir_thread.start()
