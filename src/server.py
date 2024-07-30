import socket
import threading
import sys


class Server:

    def __init__(self):
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


    def start(self, host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        address = (host, int(port))
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(address)

        sock.listen(10)

        print(f"Server running in {address[0]}:{address[1]}")


        print('waiting connections...')
        while True:
            connection, address = sock.accept()

            self.connections_alive.append(connection)

            threading.Thread(target=self.handle_client, args=(connection, address), daemon=True).start()


if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) != 3:
        print("Usage: server.py host port")
        exit(1)
    else:
        server = Server()
        server.start(sys.argv[1], sys.argv[2])