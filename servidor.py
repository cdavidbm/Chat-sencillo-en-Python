# importar librerias necesarias
import socket
import threading

# Datos de conexion
host = '127.0.0.1'
port = 55555

# Iniciar servidor
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((host, port))
servidor.listen()

# Listar clientes con apodos
clientes = []
apodos = []

# Enviar mensaje a los clientes
def difusion(mensaje):
    for cliente in clientes:
        cliente.send(mensaje)

# Manejo de la mensajería
def manejar(cliente):
    while True:
        try:
            # Difusión de la mensajeria
            mensaje = cliente.recv(1024)
            difusion(mensaje)
        except:
            # Remover clientes
            index = clientes.index(cliente)
            clientes.remove(cliente)
            cliente.close()
            apodo = apodos[index]
            difusion('{} se ha retirado!'.format(apodo).encode('ascii'))
            apodos.remove(apodo)
            break

# Funcion de recepcion
def recibir():
    while True:
        # Aceptar conexiones de nuevos clientes
        cliente, direccion = servidor.accept()
        print("Conectado {}".format(str(direccion)))

        # Solicitar y almacenar Nick
        cliente.send('NICK'.encode('ascii'))
        apodo = cliente.recv(1024).decode('ascii')
        apodos.append(apodo)
        clientes.append(cliente)

        # Anunciar la entrada del usuario a la sala
        print("apodo es {}".format(apodo))
        difusion("{} se ha unido!".format(apodo).encode('ascii'))
        cliente.send('Conecteda al servidor!'.encode('ascii'))

        # Comienza a manejar el hilo de cada clientee
        thread = threading.Thread(target=manejar, args=(cliente,))
        thread.start()

print("El servidor está escuchando...")
recibir()