import tkinter as tk
from tkinter import scrolledtext

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
            self.text_area.insert(tk.END, f"Você {msg}\n")
        elif received:
            self.text_area.insert(tk.END, f"{msg}\n")
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
