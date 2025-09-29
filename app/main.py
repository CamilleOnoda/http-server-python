from codecs import decode
import socket




def extract_url_path(request_target):
    decoded_request = request_target.decode('utf-8', errors='replace')
    request_line = decoded_request.split('\r\n')[0]
    parts = request_line.split(" ")
    if len(parts) != 3:
        raise ValueError("Malformed request line. Example: 'GET /index.html HTTP/1.1\r\n'")
    target = parts[1]
    return target


def main():
    print("Logs from my program will appear here!")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    server_socket.bind(("localhost", 4221))
    server_socket.listen(1)

    while True:
        conn, address = server_socket.accept()
        try:
            request = conn.recv(1024)
            url_path = extract_url_path(request)
            if url_path == "/":
                conn.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
            else:
                conn.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")       

        finally:
            conn.close()

if __name__ == "__main__":
    main()
