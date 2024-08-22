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
            if msg.startswith('!nick'):
                # Handle nickname setting
                _, nickname = msg.split(' ', 1)
                self.nickname = nickname
                self.sock.sendall(msg.encode())
                self.gui.display_message(f"Nickname set to: {nickname}", sent=True)
            elif msg.startswith('!sendmsg') and self.nickname:
                # Sending a message
                self.sock.sendall(f"!sendmsg {msg[9:]}".encode())
                self.gui.display_message(f"Sent: {msg[9:]}", sent=True)
            elif msg.startswith('!changenickname'):
                # Change nickname
                self.sock.sendall(msg.encode())
                self.gui.display_message(f"Requested nickname change: {msg[17:]}", sent=True)
            elif msg.startswith('!poke'):
                # Poke someone
                self.sock.sendall(msg.encode())
                self.gui.display_message(f"Requested poke: {msg[6:]}", sent=True)
            elif msg == 'exit':
                # Handle exit
                self.running = False
                self.sock.shutdown(socket.SHUT_RDWR)
            else:
                if not self.nickname and not msg.startswith('!nick'):
                    self.gui.display_message("Você deve definir um apelido com !nick antes de enviar mensagens.")
                else:
                    self.sock.sendall(msg.encode())
                    self.gui.display_message(msg, sent=True)
        except Exception as e:
            print(f"Error sending message: {e}")

    def process_message(self, msg):
        if msg.startswith("!users"):
            self.gui.display_message(f"Usuários Online: {msg[7:]}")
        elif msg.startswith("!changenickname"):
            self.gui.display_message(f"Apelido alterado: {msg[17:]}")
        elif msg.startswith("!poke"):
            self.gui.display_message(f"Você foi cutucado por {msg[6:]}")
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
