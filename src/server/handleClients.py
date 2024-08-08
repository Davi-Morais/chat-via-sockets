import threading


class Client():
    def __init__(self, connection, address) -> None:
        self.connection = connection
        self.address = address
        self.nickname = ""


class HandleClients():

    def __init__(self) -> None:
        self.listClients = []

    
    def add(self, connection, address) -> None:

        new_client = Client(connection, address)
        self.listClients.append(new_client)

        ct = threading.Thread(target=self.handle, args=(new_client,), daemon=True)
        ct.start()
        
        print(f'connection from {new_client.address}')


    def handle(self, client: Client):
        try:
            while (msg := client.connection.recv(2048)):
                self.broadcast(client, msg)               
        
        finally:
            self.listClients.remove(client)
            print(len(self.listClients))
            client.connection.close()
            print(f"Connection with {client.address} closed!")


    def broadcast(self, sender, msg) -> None:
        for client in self.listClients:
            try:
                if client is not sender:
                    client.connection.sendall(msg)
            except Exception as e:
                print(e)