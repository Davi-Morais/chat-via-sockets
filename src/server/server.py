import socket
import threading


class Server:

    def __init__(self, host, port):
        self.host = host
        self.port = int(port)
        self.connections_alive = []


    def broadcast(self, sender, address, msg):
        for connection in self.connections_alive:
            try:
                if connection != sender:
                    connection.sendall(msg)
            except Exception as e:
                print(e)


    def handle_client(self, connection, address):
        print(f'connection from {address}')

        try:
            while (msg := connection.recv(2048)):
                self.broadcast(connection, address, msg)               
        
        finally:
            self.connections_alive.remove(connection)
            print(len(self.connections_alive))
            connection.close()
            print(f"Connection with {address} closed!")


    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        address = (self.host, self.port)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(address)

        sock.listen(10)

        print(f"Server running in {address[0]}:{address[1]}")


        print('waiting connections...')
        while True:
            connection, address = sock.accept()

            self.connections_alive.append(connection)

            threading.Thread(target=self.handle_client, args=(connection, address), daemon=True).start()