import socket
import threading

class ChatServer:
    def __init__(self, host='172.29.17.106', port=55555):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()
        self.clients = []
        self.nicknames = []
        
    def broadcast(self, message, sender_client=None):
        for client in self.clients:
            if client != sender_client:  # Filtro para no enviar el mensaje al cliente que lo envió
                client.send(message)
    
    def handle_client(self, client):
        while True:
            try:
                message = client.recv(1024).decode('utf-8')
                
                if message.lower() == 'exit':
                    # Desconectar al cliente si envía "exit"
                    self.disconnect_client(client)
                    break
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
            
            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()
    
    def start(self):
        self.receive()

if __name__ == "__main__":
    server = ChatServer()
    server.start()