from .server import Server
from .constants import HOST, PORT

def main():
    print("Logs from my program will appear here!")

    Server(HOST,PORT).server_forever()

if __name__ == "__main__":
    main()
