import socket
import threading

class Client:
    def __init__(self, host, port, gui):
        self.host = host
        self.port = int(port)
        self.sock = None
        self.running = True
        self.gui = gui
        self.nickname = ""

    def read_input(self):
        while self.running:
            try:
                msg = self.sock.recv(2048).decode()
                if msg:
                    self.process_message(msg)
                else:
                    break
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

        self.close_connection()

    def send_message(self, msg):
        try:
            if not self.nickname and msg:
                # _, nickname = msg.split(' ', 1)
                self.nickname = msg
                self.sock.sendall(f"!nick {msg}".encode())
                self.gui.display_message(f"é {self.nickname}", sent=True)                
                


            elif msg.startswith('!changenickname'):
                # Change nickname
                self.sock.sendall(msg.encode())
                # self.gui.display_message(f"Requested nickname change: {msg[17:]}", sent=True)
            elif msg.startswith('!poke'):
                # Poke someone
                self.sock.sendall(msg.encode())
                # self.gui.display_message(f"Requested poke: {msg[6:]}", sent=True)
            elif msg == 'exit':
                # Handle exit
                self.running = False
                self.sock.shutdown(socket.SHUT_RDWR)
            else:

                self.sock.sendall(f"!sendmsg {msg}".encode())
                    # self.gui.display_message(f"Sent: {msg}", sent=True) # Talvez tirar
                    # self.sock.sendall(msg.encode())
                    # self.gui.display_message(msg, sent=True)
        except Exception as e:
            print(f"Error sending message: {e}")

    def process_message(self, msg):
        if msg.startswith("!users"):
            command, num_user, users = msg.strip(' ').split(' ', 2)
            if int(num_user) > 1:
                self.gui.display_message(f"{num_user} usuários online: {users}")
            else:
                self.gui.display_message(f"{num_user} usuário online: {users}")
        elif msg.startswith("!changenickname"):
            command, old_name, new_name = msg.strip(' ').split(' ', 2)
            self.gui.display_message(f"{old_name} agora é {new_name}!")
        elif msg.startswith("!poke"):
            command, user, poked_user = msg.strip(' ').split(' ', 2)
            self.gui.display_message(f"{user} cutucou {poked_user}")
        elif msg.startswith("!left"):
            self.gui.display_message(f"{msg[6:]} saiu.")
        elif msg.startswith("!msg"):
            # Extracting the sender nickname and message
            parts = msg.split(' ', 2)
            if len(parts) >= 3:
                sender = parts[1]
                message = parts[2]
                self.gui.display_message(f"{sender}: {message}", received=True)
        else:
            self.gui.display_message(msg, received=True)

    def start(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = (self.host, self.port)
            self.sock.connect(server_address)
            print(f'Connecting to {server_address[0]} port {server_address[1]}')

            thread = threading.Thread(target=self.read_input, daemon=True)
            thread.start()

        except Exception as e:
            print(f"Connection error: {e}")
            self.gui.display_message(f"Connection error: {e}")
            self.close_connection()

    def close_connection(self):
        if self.sock:
            self.sock.close()
        self.gui.display_message("Connection closed!", received=True)
        self.running = False
        self.gui.close()
