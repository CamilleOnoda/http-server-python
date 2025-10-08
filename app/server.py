import socket
from .http import get_header, get_url, handle_request
from .constants import HOST, PORT, HTTP_CODE_404


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def server_forever(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        print(f"Server listening on: {HOST}, {PORT}")

        while True:
            conn, address = server_socket.accept()
            try:
                raw_request = conn.recv(1024)
                url_path = get_url(raw_request)
                user_agent = get_header(raw_request, "User-Agent") or ""
                response = handle_request(url_path, user_agent)
                conn.sendall(response)
            finally:
                conn.close()