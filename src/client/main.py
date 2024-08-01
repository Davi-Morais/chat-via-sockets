from client import Client
import sys


if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) != 3:
        print("Usage: client.py host port")
        exit(1)
    else:
        client = Client(sys.argv[1], sys.argv[2])
        client.start()