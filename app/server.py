import socket
from .http import extract_url_path
from .constants import HOST, PORT, HTTP_CODE_200, HTTP_CODE_404


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def server_forever(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)

        while True:
            conn, address = server_socket.accept()
            try:
                raw_request = conn.recv(1024)
                url_path = extract_url_path(raw_request)
                if url_path == "/":
                    conn.sendall(HTTP_CODE_200.encode())
                else:
                    conn.sendall(HTTP_CODE_404.encode())       
            finally:
                conn.close()