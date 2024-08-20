import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
import sys

class Client:
    def __init__(self, host, port, gui):
        self.host = host
        self.port = int(port)
        self.sock = None
        self.running = True
        self.gui = gui

    def read_input(self):
        while self.running:
            try:
                msg = self.sock.recv(2048)
                if not msg:
                    break
                self.gui.display_message(msg.decode(), received=True)
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

        self.close_connection()

    def send_message(self, msg):
        try:
            if msg != 'exit':
                self.sock.sendall(msg.encode())
                self.gui.display_message(msg, sent=True)
            else:
                self.running = False
                self.sock.shutdown(socket.SHUT_RDWR)
        except Exception as e:
            print(f"Error sending message: {e}")

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

class ClientGUI:
    def __init__(self, master):
        self.master = master
        master.title("Client")

        self.text_area = scrolledtext.ScrolledText(master, wrap=tk.WORD, height=15, width=50)
        self.text_area.pack(padx=10, pady=10)

        self.entry = tk.Entry(master, width=50)
        self.entry.pack(side=tk.LEFT, padx=10, pady=10)
        self.entry.bind('<Return>', self.on_send)

        self.send_button = tk.Button(master, text="Send", command=self.on_send)
        self.send_button.pack(side=tk.RIGHT, padx=10, pady=10)

    def display_message(self, msg, sent=False, received=False):
        if sent:
            self.text_area.insert(tk.END, f"Você: {msg}\n")
        elif received:
            self.text_area.insert(tk.END, f"Server: {msg}\n")
        else:
            self.text_area.insert(tk.END, f"{msg}\n")
        self.text_area.yview(tk.END)

    def on_send(self, event=None):
        msg = self.entry.get()
        if msg:
            self.client.send_message(msg)
            self.entry.delete(0, tk.END)

    def set_client(self, client):
        self.client = client

    def close(self):
        self.master.destroy()

def main():
    if len(sys.argv) != 3:
        print("Usage: client.py host port")
        sys.exit(1)

    host = sys.argv[1]
    port = sys.argv[2]

    root = tk.Tk()
    gui = ClientGUI(root)
    client = Client(host, port, gui)
    gui.set_client(client)
    client.start()
    root.mainloop()

if __name__ == "__main__":
    main()
