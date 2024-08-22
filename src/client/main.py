import sys
import tkinter as tk
from client import Client
from gui import ClientGUI

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
