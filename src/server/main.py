from server import Server 
import sys


if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) != 3:
        print("Usage: server.py host port")
        exit(1)
    else:
        server = Server(sys.argv[1], sys.argv[2])
        server.start()