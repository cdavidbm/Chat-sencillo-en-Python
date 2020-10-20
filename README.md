# CHAT SIMPLE EN PYTHON

Para nuestro modulo, usamos la arquitectura cliente-servidor. Esto significa que tendremos varios clientes (los usuarios) y un servidor central que alojara todo y proporcionara los datos para estos clientes. Por lo tanto, necesitamos escribir dos scripts de Python. Uno sera para iniciar el servidor y el otro sera para el cliente. Primero se ejecuta en el servidor para que haya una sala de chat a la que los clientes puedan conectarse. Los propios clientes no se comunicaran directamente entre si, sino a traves del servidor central. 

### IMPLEMENTANDO EL SERVIDOR:

Comenzamos implementando el servidor. Para esto, necesitamos importar dos bibliotecas: `socket` y `threading`. La primera se utilizara para la conexion a la red y la segunda es para que Python pueda realizar varias tareas al mismo tiempo, es decir, que no funcione linealmente como un Script. 

```
import socket
import threading
```

Lo siguiente es definir los datos de conexion e inicializar el servidor. Necesitamos una direccion IP para el host y un numero de puerto libre para el servidor. En este caso, usamos la direccion localhost (127.0.0.1) y el puerto 55555.
 
```
host = '127.0.0.1'
port = 55555
```

Cuando definimos el servidor, es necesario pasar dos parametros. Estos definen el tipo de socket que queremos usar. El primero `AF_INET`, indica que estamos usando un conector de Internet en lugar de un conector del sistema. El segundo parametro representa el protocolo que queremos usar, `SOCK_STREAM`  indica que estamos usando TCP y no UDP:  

```
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
```

Despues de definir el socket, lo vinculamos al host y al puerto especificado. Luego, ponemos el servidor en modo de escucha, para que espere a que los clientes se conecten: 

```
servidor.bind((host, port))
servidor.listen()
```

Al final creamos dos listas vacias, que usaremos para almacenar los clientes conectados y sus apodos mas adelante: 

```
clientes = []
apodos = []
```

Ahora definimos la funcion que transmite los mensajes a cada cliente que este conectado:

```
def difusion(mensaje):
    for cliente in clientes:
        cliente.send(mensaje)
```

Ahora viene la funcion que maneja los mensajes de los clientes. Esta funcion se ejecuta en un ciclo while. No se detendra a menos que haya una excepcion debido a algo que salga mal. La funcion acepta un cliente como parametro. Cada vez que un cliente se conecta al servidor, se ejecuta esta funcion y comienza un ciclo sin fin.

Entonces, lo que hace es recibir el mensaje del cliente (si envia alguno) y transmitirlo a todos los clientes conectados. Entonces, cuando un cliente envia un mensaje, todos los demas pueden ver este mensaje. Los mensajes son codificados al enviarse y decodificados al ser recibidos, pues solo podemos enviar bytes y no cadenas, para eso utilizamos el parametro `encode('ascii')`. 

Ahora bien, si por alguna razon hay un error con la conexion a este cliente o el cierra su sesion, lo eliminamos, cerramos la conexion y transmitimos que este cliente ha salido del chat. Despues de eso, rompemos el bucle y llega a su fin.

```
def manejar(cliente):
    while True:
        try:
            # Difusion de la mensajeria
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
```

 Funcion de recepcion: tambien inicia un ciclo while sin fin, que acepta constantemente nuevas conexiones de los clientes. Una vez que un cliente esta conectado, le envia la cadena  `'NICK'`, solicitando el nombre de usuario. Despues de eso, espera una respuesta (el Nick) y agrega al cliente a la sala. Despues de eso, se comunica esa informacion a la sala.  

```
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

        # Comienza a manejar el proceso de cada clientee
        thread = threading.Thread(target=manejar, args=(cliente,))
        thread.start() 
```

Utilizamos la siguiente instruccion para anunciar que el servidor esta listo y llamamos la funcion de recepcion: 

```
print("El servidor esta escuchando...")
recibir()
```

### IMPLEMENTACION DEL CLIENTE:

Nuevamente necesitaremos importar las mismas bibliotecas:
 
```
import socket
import threading 
```

Lo primero que debe hacer el cliente es elegir un apodo y conectarse al servidor. El script del cliente necesita saber la direccion y el puerto en el que se esta ejecutando el servidor. Ahora usamos una funcion diferente, en lugar de vincular los datos y escuchar, nos estamos conectando a un servidor existente.  

```
# El cliente elige un nombre
apodo = input("Indique un nombre para ingresar a la sala: ")

# Conectarse al servidor
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(('127.0.0.1', 55555))
```

Ahora, el cliente debe tener dos subprocesos. El primero recibe constantemente datos del servidor y el segundo envia los mensajes del cliente al servidor. De nuevo, aqui tenemos un ciclo while sin fin. Constantemente intenta recibir mensajes e imprimirlos en la pantalla. Si el mensaje es `'NICK'`, no lo imprime pero envia el apodo al servidor. En caso de que haya algun error, se cierra la conexion y se rompe el bucle: 

```
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
```

La funcion de escritura se ejecuta en un bucle sin fin que siempre esta esperando una entrada del usuario. Una vez que obtiene algo, lo combina con el apodo y lo envia al servidor. Despues, lo ultimo que debemos hacer es iniciar los dos subprocesos que ejecutan estas funciones: 

```
# Enviar mensajes al servidor
def escribir():
    while True:
        mensaje = '{}: {}'.format(apodo, input(''))
        cliente.send(mensaje.encode('ascii'))

# Iniciar proceso de conversacion. Escuchar y escribir
recibir_thread = threading.Thread(target=recibir)
recibir_thread.start()

escribir_thread = threading.Thread(target=escribir)
escribir_thread.start()
```
