import socket
from .http import extract_url_path
from constants import HOST, PORT, HTTP_CODE_200, HTTP_CODE_404


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def server_forever():
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)

        while True:
            conn, address = server_socket.accept()
            try:
                request = conn.recv(1024)
                url_path = extract_url_path(request)
                response_200 = HTTP_CODE_200.encode()
                response_404 = HTTP_CODE_404.encode()
                if url_path == "/":
                    conn.sendall(response_200)
                else:
                    conn.sendall(response_404)       
            finally:
                conn.close()