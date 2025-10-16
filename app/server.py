import socket, threading
from .http import get_header, get_url, handle_request
from .constants import END_HEADERS, HOST, PORT


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port


    def _recv_request(self, conn):
        buffer = b""
        terminator = END_HEADERS.encode("utf-8")
        while terminator not in buffer:
            chunk = conn.recv(4096)
            if not chunk:
                break
            buffer += chunk
        return buffer


    def handle_client(self, conn, sem):
        print(f"[{threading.current_thread().name}] Handling request", flush=True)
        try:
            raw_request = self._recv_request(conn)
            if not raw_request:
                conn.close()
        
            url_path = get_url(raw_request)
            user_agent = get_header(raw_request, "User-Agent") or ""
            response = handle_request(url_path, user_agent)
            conn.sendall(response)
        except Exception as e:
            print("ERROR: ", repr(e))
            conn.sendall(b"HTTP/1.1 400 Bad Request\r\nContent-Length: 0\r\n\r\n")
        finally:
            conn.close()
            sem.release()


    def server_forever(self):
        sem = threading.Semaphore(8)
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        server_socket.bind(("127.0.0.1", 4221))
        server_socket.listen(64)
        print(f"Server listening on: {self.host}, {self.port}")

        while True:
            conn, addr = server_socket.accept()
            sem.acquire()
            client_thread = threading.Thread(
                target=self.handle_client,
                args=(conn,sem),
                name=f"Client-{addr}",
                daemon=True) #False → cleaner, ensures all threads finish (better for production-style behavior)
            client_thread.start()


if __name__ == "__main__":
    Server(HOST, PORT).server_forever()