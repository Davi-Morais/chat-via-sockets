
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

        print(f'connection from {new_client.address}')

        try:
            while (msg := new_client.connection.recv(2048)):
                self.broadcast(new_client, msg)               
        
        finally:
            self.listClients.remove(new_client)
            print(len(self.listClients))
            new_client.connection.close()
            print(f"Connection with {new_client.address} closed!")


    def broadcast(self, sender, msg) -> None:
        for client in self.listClients:
            try:
                if client is not sender:
                    client.connection.sendall(msg)
            except Exception as e:
                print(e)