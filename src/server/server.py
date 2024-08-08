import socket
import threading
from handleClients import HandleClients


class Server:

    def __init__(self, host, port):
        self.host = host
        self.port = int(port)
        self.connections_alive = []


    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        host_port = (self.host, self.port)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(host_port)

        sock.listen(10)

        handleClients = HandleClients()

        print(f"Server running in {host_port[0]}:{host_port[1]}")
        print('waiting connections...')
        while True:
            connection, address = sock.accept()

            ct = threading.Thread(target=handleClients.add, args=(connection, address), daemon=True)
            ct.start()