import socket


def main():
    print("Logs from my program will appear here!")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    server_socket.bind(("localhost", 4221))
    server_socket.listen()

    while True:
        conn, address = server_socket.accept()
        conn.close()

if __name__ == "__main__":
    main()
