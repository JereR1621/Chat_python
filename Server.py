import socket
import threading

class ChatServer:
    def __init__(self, host='10.1.5.74', port=55555):
        self.fileSave = open("testFile.txt","w")
        self.fileSave.close()
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()
        self.clients = []
        self.nicknames = []

              
    def comand(self,signal,sender_client=None):
        print("SYS>> datos servidor:  "+self.hos+" "+str(self.port))
        
    def broadcast(self, message, sender_client=None):
        self.fileSave = open("testFile.txt","ab")
        print(message)
        for client in self.clients:
            self.fileSave.write(message)    
            self.fileSave.write(b'\n')
            if(client == None):
                msgSYS = "SYS>>"+message
                client.send(msgSYS)
            if client != sender_client:  # Filtro para no enviar el mensaje al cliente que lo envió
                client.send(message)
                
        self.fileSave.close(    )

    def cargarMensajes(self,archTxt = None,sender_client = None):
        self.fileSave = open("testFile.txt",'wb+')
        if not self.fileSave.read(1):
            return
        for line in self.fileSave:
            tes =line.encode('utf-8')
            sender_client.send(tes)
        self.fileSave.close()


    def handle_client(self, client):
        while True:
            try:
                message = client.recv(1024).decode('utf-8')
                
                if message.lower() == 'exit':
                    # Desconectar al cliente si envía "exit"
                    self.disconnect_client(client)
                    break
                elif(message.lower()=="server"):
                    msg = "Datos servidor: "+self.host+" "+str(self.port)
                    self.broadcast(msg.encode('utf-8'))
                else:
                    # Si no es "exit", se considera un mensaje normal
                    self.broadcast(message.encode('utf-8'), sender_client=client)
            except:
                # Manejar desconexión inesperada
                self.disconnect_client(client)
                break

    def disconnect_client(self, client):
        """Maneja la desconexión de un cliente."""
        if client in self.clients:
            index = self.clients.index(client)
            nickname = self.nicknames[index]
            self.clients.remove(client)
            self.nicknames.remove(nickname)
            client.close()
            self.broadcast(f'{nickname} ha abandonado el chat!'.encode('utf-8'))
            print(f"Cliente {nickname} desconectado")
    
    def receive(self):
        print("Servidor iniciado y escuchando...")
        print(self.host)
        print(self.port)
        while True:
            client, address = self.server.accept()
            print(f"Conectado con {str(address)}")
            
            client.send('NICK'.encode('utf-8'))
            nickname = client.recv(1024).decode('utf-8')
            self.nicknames.append(nickname)
            self.clients.append(client)
            
            print(f"Nickname del cliente es {nickname}!")
            self.broadcast(f"{nickname} se ha unido al chat!".encode('utf-8'))
            client.send('Conectado al servidor!'.encode('utf-8'))
            self.cargarMensajes(client)
            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()
    
    def start(self):
        self.receive()

if __name__ == "__main__":
    server = ChatServer()
    server.start()