import socket
import threading


class Client():

    def __init__(self, host, port):
        self.host=host
        self.port=port
        
    def read_input(self, sock):
        while (msg := input()):
            if msg != 'exit':
                sock.sendall(msg.encode())
            else:
                sock.shutdown(socket.SHUT_RDWR)
                sock.close()
            

    def start(self):
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (self.host, int(self.port))

        sock.connect(server_address)
        print(f'connecting to {server_address[0]} port {server_address[1]}')

        thread = threading.Thread(target=self.read_input, args=(sock,), daemon=True)
        thread.start()

        try:
            while (msg := sock.recv(2048)):
                print(msg.decode())

        finally:
            print("Connection closed!")
            exit(0)