import socket, threading
from app.config import ServerConfig
from .http import handle_request
from .constants import (END_HEADERS_BYTES, END_HEADERS, CRLF,
                        HTTP_CODE_400, HTTP_CODE_408, 
                        HTTP_CODE_413, HTTP_CODE_501)
from .request import Request, NotImplementedTE, BadRequest


class Server:
    def __init__(self, config: ServerConfig):
        self.config = config


    def _recv_request_headers(self, conn: socket.socket) -> tuple[bytes, bytes]:
        """
        Returns (header_bytes, body_prefix).\n
        Reads until \r\n\r\n but might receive early body bytes.
        """
        try:
            conn.settimeout(self.config.recv_time_out)
            buffer = bytearray()
            end = END_HEADERS_BYTES
            max_headers = self.config.max_headers_bytes

            while True:
                chunk = conn.recv(4096)
                if not chunk:
                    break
                buffer += chunk
                if end in buffer:
                    break
                if len(buffer) > max_headers:
                    raise BadRequest("Header section too large.")

            if end not in buffer:
                raise BadRequest("Header section incomplete.") 

            head_end = buffer.index(end) + len(end)
            header_bytes = bytes(buffer[:head_end])
            body_prefix = bytes(buffer[head_end:])
            return header_bytes, body_prefix
        except socket.timeout:
            self._send_error(conn, HTTP_CODE_408, "Request Timeout")
    

    def _read_request_body(self, conn: socket.socket, req: Request) -> None:
        """
        Reads exactly Content-Length bytes starting from body_prefix.
        Verify max_body_bytes and enforce no over-read.
        """
        total = req.content_length or 0
        if total == 0:
            req.add_body(b"")
            return
        
        if total > self.config.max_body_bytes:
            raise PayloadTooLarge()
        
        body = bytearray(req.body_prefix)
        if len(body) > total:
            body = body[:total]

        while len(body) < total:
            chunk = conn.recv(min(4096, total - len(body)))
            if not chunk:
                raise IncompleteBody()
            body += chunk
    
        req.add_body(bytes(body))


    def _send_error(self,
                    conn: socket.socket, 
                    status_line: str, 
                    reason: str = ""
                    ) -> None:
        body = reason.encode("utf-8")
        head = CRLF.join([
            status_line,
            "Content-Type: text/plain",
            f"Content-Length: {len(body)}",
            "Connection: close",
        ]) + END_HEADERS
        try:
            conn.sendall(head.encode("utf-8") + body)
        except Exception as e:
            print(f"ERROR: {str(e)}")


    def handle_client(self,
                      conn: socket.socket,
                      sem: threading.Semaphore,
                      lock: threading.Lock
                      ) -> None:
        with lock:
            print(f"[{threading.current_thread().name}] Handling request",
                  flush=True)
        try:
            header_bytes, body_prefix = self._recv_request_headers(conn)
            req = Request.create_request_instance(header_bytes,
                                                  body_prefix, 
                                                  remote_addr=conn.getpeername())
            if (req.content_length or 0) > self.config.max_body_bytes:
                raise PayloadTooLarge()
            if req.read_body():
                self._read_request_body(conn, req)
            else:
                req.add_body(b"")
            
            response = handle_request(req, self.config.root_dir)
            conn.sendall(response)

        except NotImplementedTE:
            self._send_error(conn, HTTP_CODE_501, 
                             "Transfer-Encoding: chunked"
                             " is not supported")
        except PayloadTooLarge:
            self._send_error(conn, HTTP_CODE_413, "Payload Too Large")
        except IncompleteBody:
            self._send_error(conn, HTTP_CODE_408, "Request body incomplete")
        except (BadRequest, ValueError) as e:
            self._send_error(conn, HTTP_CODE_400, str(e))
        except Exception as e:
            self._send_error(conn, HTTP_CODE_400, str(e))
        
        finally:
                conn.close()
                sem.release()


    def serve_forever(self):
        sem = threading.Semaphore(self.config.max_concurrent_connections)
        lock = threading.Lock()
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        server_socket.bind((self.config.host, self.config.port))
        server_socket.listen(64)
        print(f"Server listening on: {self.config.host}, {self.config.port}")

        while True:
            conn, addr = server_socket.accept()
            sem.acquire()
            client_thread = threading.Thread(
                target=self.handle_client,
                args=(conn, sem, lock),
                name=f"Client-{addr}",
                daemon=False)
            client_thread.start()


class PayloadTooLarge(Exception):
    pass

class IncompleteBody(Exception):
    pass
