import socket
import threading

class ChatClient:
    def __init__(self, host='172.29.17.106', port=55555):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.nickname = None
        
    def receive(self):
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.client.send(self.nickname.encode('utf-8'))
                else:
                    print(message)
            except:
                print("Error! Conexión cerrada.")
                self.client.close()
                break
    
    def write(self):
        while True:
            message = input("")
            if message.lower() == 'exit':
                # Enviar "exit" al servidor indicando que el cliente se desconecta
                self.client.send("exit".encode('utf-8'))
                print("Desconectando...")
                self.client.close()
                break
            else:
                # Enviar mensaje normal al servidor
                self.client.send(f'{self.nickname}: {message}'.encode('utf-8'))
    
    def start(self):
        self.nickname = input("Elige un nickname: ")
        
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()
        
        write_thread = threading.Thread(target=self.write)
        write_thread.start()

if __name__ == "__main__":
    client = ChatClient()
    client.start()