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

                client.connection.sendall(self.users_online().encode())

                while (data := client.connection.recv(2048)):

                    command = data.decode(encoding='UTF-8').split(' ', 1)
        
                    if command[0] == '!sendmsg':
                        self.broadcast(client, command[1])
                    elif command[0] == '!changenickname':
                        self.changenickname(client, command[1])
                    
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

        except Exception as e:
            print(e)
            

    def changenickname(self, client: Client, new_nickname):
        old_nickname = client.nickname
        client.nickname = new_nickname
        
        b_msg = f'changenickname {old_nickname} {client.nickname}'.encode()

        for c in self.listClients:
            c.connection.sendall(b_msg)


    def users_online(self):
        number_of_users = len(self.listClients)
        nickname_of_all_users = self.getNickUsers()

        return f"!users {number_of_users} {nickname_of_all_users}"


    def getNickUsers(self) -> str:
        nicknames = [user.nickname for user in self.listClients]
        return " ".join(nicknames)


    def broadcast(self, sender, msg) -> None:

        b_msg = f'!msg {sender.nickname} {msg}'.encode()

        for client in self.listClients:
            try:
                if client is not sender:
                    client.connection.sendall(b_msg)
            except Exception as e:
                print(e)
