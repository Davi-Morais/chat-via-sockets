import socket
import sys
import threading


def read_input(sock):
    while (msg := input()):
        if msg != 'exit':
            sock.sendall(msg.encode())
        else:
            sock.shutdown(socket.SHUT_RDWR)
            sock.close()
        

def client(host, port):
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (host, int(port))

    sock.connect(server_address)
    print(f'connecting to {server_address[0]} port {server_address[1]}')

    thread = threading.Thread(target=read_input, args=(sock,), daemon=True)
    thread.start()

    try:
        while (msg := sock.recv(2048)):
            print(msg.decode())

    finally:
        print("Connection closed!")
        exit(0)


if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) != 3:
        print("Usage: client.py host port")
        exit(1)
    else:
        client(sys.argv[1], sys.argv[2])