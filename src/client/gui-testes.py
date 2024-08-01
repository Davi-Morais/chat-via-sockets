import tkinter as Tk
from client import Client 

root = Tk.Tk()

def submit(Client):
    print("entered text were ") + entry.get()

entry = Tk.Entry(root)
entry.pack()
button = Tk.Button(root,text='submit',command=submit)
button.pack()

root.mainloop()
