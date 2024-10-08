import threading
import socket


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

                users_online = self.users_online().encode()
                for c in self.listClients:
                    c.connection.sendall(users_online)


                while (data := client.connection.recv(2048)):

                    command = data.decode(encoding='UTF-8')
                    command = command.strip('\r\n').strip(' ')
        
                    if command.startswith('!sendmsg '):
                        self.broadcast(client, command[9:])
                    elif command.startswith('!changenickname '):
                        self.changenickname(client, command[16:])
                    elif command.startswith('!poke '):
                        self.poke(client, command[6:])
                    elif command.startswith('!left'):
                        client.connection.shutdown(socket.SHUT_RDWR)
                    
        finally:
            if client in self.listClients:
                self.listClients.remove(client) 
            self.left(client)
            print(len(self.listClients))
            client.connection.close()
            print(f"Connection with {client.address} closed!")


    def setNickname(self, client: Client):
        try:
            data = client.connection.recv(2048)

            command = data.decode(encoding='UTF-8')
            command = command.strip('\r\n')

            if command.startswith('!nick ') and len(command) > 5:
                client.nickname = command[6:]

        except Exception as e:
            print(e)
            

    def changenickname(self, client: Client, new_nickname):
        old_nickname = client.nickname
        client.nickname = new_nickname
        
        b_msg = f'!changenickname {old_nickname} {client.nickname}'.encode()

        for c in self.listClients:
            c.connection.sendall(b_msg)


    def users_online(self):
        number_of_users = len(self.listClients)
        nickname_of_all_users = self.getNickUsers()

        return f"!users {number_of_users} {nickname_of_all_users}"


    def getNickUsers(self) -> str:
        nicknames = [user.nickname for user in self.listClients]
        return " ".join(nicknames)

    
    def get_user_by_nickname(self, nickname: str):
        for c in self.listClients:
            if c.nickname == nickname:
                return c


    def poke(self, client:Client, poked_nickname):
        poked_user = self.get_user_by_nickname(poked_nickname)

        if poked_user and (poked_user.nickname == poked_nickname):
            b_msg = f'!poke {client.nickname} {poked_user.nickname}'.encode()

            for c in self.listClients:
                c.connection.sendall(b_msg)


    def broadcast(self, sender, msg) -> None:

        b_msg = f'!msg {sender.nickname} {msg}'.encode()

        for client in self.listClients:
            try:
                # if client is not sender: ###
                client.connection.sendall(b_msg)
            except Exception as e:
                print(e)


    def left(self, sender:Client):
        b_msg = f'!left {sender.nickname}'.encode()
        
        for c in self.listClients:
            if c is not sender:
                c.connection.sendall(b_msg)

