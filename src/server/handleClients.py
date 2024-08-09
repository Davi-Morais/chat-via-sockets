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

        ct = threading.Thread(target=self.handle, args=(new_client,), daemon=True)
        ct.start()
        
        print(f'connection from {new_client.address}')


    def handle(self, client: Client):
        try:
            self.setNickname(client)

            if client.nickname:
                self.listClients.append(client)

                while (msg := client.connection.recv(2048)):
                    self.broadcast(client, msg)               
        
        finally:
            if client in self.listClients:
                self.listClients.remove(client)
            print(len(self.listClients))
            client.connection.close()
            print(f"Connection with {client.address} closed!")


    def setNickname(self, client: Client):
        try:
            data = client.connection.recv(2048)

            command = data.decode(encoding='UTF-8').split(' ', 1)

            if command[0] == '!nick' and len(command) == 2:
                client.nickname = command[1]

                number_of_users = len(self.listClients)
                nickname_of_all_users = self.getNickUsers()

                nicksnames_msg = f"!users {number_of_users} {nickname_of_all_users}"

                client.connection.sendall(nicksnames_msg.encode())

        except Exception as e:
            print(e)
            


    def getNickUsers(self) -> str:
        nicknames = [user.nickname for user in self.listClients]
        return " ".join(nicknames)


    def broadcast(self, sender, msg) -> None:
        for client in self.listClients:
            try:
                if client is not sender:
                    client.connection.sendall(msg)
            except Exception as e:
                print(e)