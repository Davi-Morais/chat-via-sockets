import socket
import threading
import sys


class Server:

    def handle_client(self, connection, client_address):
        print(f'connection from {client_address}')

        try:
            while (data := connection.recv(2048)):
                msg = data.decode('utf-8')
                print(f"{msg}")
                
        
        finally:
            connection.close()
            print(f"Connection with {client_address} closed!")


    def start(self, host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        address = (host, int(port))
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(address)

        sock.listen(10)

        print(f"Server running in {address[0]}:{address[1]}")


        print('waiting connections...')
        while True:
            connection, client_address = sock.accept()

            threading.Thread(target=self.handle_client, args=(connection, client_address), daemon=True).start()


if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) != 3:
        print("Usage: server.py host port")
        exit(1)
    else:
        server = Server()
        server.start(sys.argv[1], sys.argv[2])