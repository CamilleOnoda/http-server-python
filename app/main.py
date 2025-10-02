from .server import Server


def main():
    print("Logs from my program will appear here!")

    Server().server_forever()

if __name__ == "__main__":
    main()
