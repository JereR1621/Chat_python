import socket
import threading
import re
class ChatClient:
    def __init__(self, host='192.168.0.251', port=55555):
        
        self.estadoConexion = 0
        while(self.estadoConexion==0):
            try:
                self.host = host
                self.port = port
                self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client.connect((host, port))
                self.nickname = None
                self.estadoConexion = 1
            except:
                print("SYS>> error, no se a detectado servidor o la IP que esta introducida no es valida")
                inpt = input("SYS>> desea conectar a una ip distinta a "+host+"?       Y/n:  ")
                if(inpt == "Y"):
                    ip =     input("..")
                    if(self.valIP(ip)):
                        host = ip
                    else:
                        print("IP invalida")
                elif(inpt == "n"):
                    return
    def valIP(self, ip):
        forma = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
        if not forma.match(ip):
            return 0
        partes = ip.split('.')
        return all(0 <= int(p) <= 255 for p in partes)

    def serverConect(self,port=55555):
        while True:
            ipIn = input("IP de servidor deseado... : ")
            if not self.valIP(ipIn):
                print("IP invalida")
                t = input("SYS>> si desea conectar al servidor original introdusca 'T'")
                if(t != "T"):
                    continue
                else:
                    host = '192.168.0.251'
            self.estadoConexion = 0
            while(self.estadoConexion==0):
                try:
                    self.host = host
                    self.port = port
                    self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.client.connect((host, port))
                    self.nickname = None
                    self.estadoConexion = 1
                except:
                    print("SYS>> error, no se a detectado servidor o la IP que esta introducida no es valida")
                    t = input("SYS>> si desea conectar al servidor original introdusca 'T'")
                    host = '192.168.0.251'
                    if(t != "T"):
                        inpt = input("SYS>> desea conectar a una ip distinta a "+host+"?       Y/n")
                        if(inpt == "Y"):
                            ip =     input("..")
                            if(self.valIP(ip)):
                                host = ip
                            else:
                                print("IP invalida")
                        elif(inpt == "n"):
                            return

    def receive(self):
        while True:
            if(self.endSignal == 1):
                break
            try:
                data =self.client.recv(1024)
                if(data==0):
                    print("SYS>> servidor cerrado por host")
                    self.endSignal = 1
                    self.client.close();
                    break
                message = data.decode('utf-8')
                

                if message == 'NICK':
                    self.client.send(self.nickname.encode('utf-8'))
                else:
                    print(message)
            except Exception as e:
                #print("Error! Conexión cerrada."+str(e))
                self.endSignal = 1
                self.client.close()
                break
    
    def write(self):
        while True :
            if(self.endSignal ==1):
                break
            message = input("")
            if(len(message)<= 0):
                continue
            if message.lower() == '/exit':
                # Enviar "exit" al servidor indicando que el cliente se desconecta
                self.client.send("exit".encode('utf-8'))
                print("Desconectando...")
                self.endSignal = 1
                self.client.close()
                break
            elif message.lower() == "/change":
                print("SYS>> cambiando servidor...")
                self.endSignal = 1
                self.client.close()

                break
            elif message.lower() == '/ip':
                print("SYS>> Su ip es::  "+self.host)
            elif message.lower() == '/prt':
                print("SYS>> Su puerto es::  "+str(self.client.getsockname()[1]))
            elif message.lower() == '/server':
                self.client.send("server".encode('utf-8'))
            else:
                # Enviar mensaje normal al servidor
                self.client.send(f'{self.nickname}: {message}'.encode('utf-8'))
    
    def start(self):
        if(self.estadoConexion==0): return
        self.nickname = input("Elige un nickname: ")
        self.endSignal = 0 # si señan final es 1, verdadero, entonces en "recieve" terminara antes de recibir cualquier error
        self.receive_thread = threading.Thread(target=self.receive)
        self.receive_thread.start()
        
        self.write_thread = threading.Thread(target=self.write)
        self.write_thread.start()

if __name__ == "__main__":
    client = ChatClient()
    client.start()