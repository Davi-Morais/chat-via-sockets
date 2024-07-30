import socket
import sys
import threading


def recv_msg(sock):
    while (msg := sock.recv(2048)):
        print(msg.decode())

def client(host, port):
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (host, int(port))

    sock.connect(server_address)

    threading.Thread(target=recv_msg, args=(sock,), daemon=True).start()

    try:

        print(f'connecting to {server_address[0]} port {server_address[1]}')

        while (msg := input('> ')) != 'exit':
            sock.sendall(msg.encode())

    finally:
        sock.close()
        print("Connection closed!")


if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) != 3:
        print("Usage: client.py host port")
        exit(1)
    else:
        client(sys.argv[1], sys.argv[2])