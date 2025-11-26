from .constants import CRLF, END_HEADERS, HTTP_CODE_200, HTTP_CODE_201, HTTP_CODE_404
from pathlib import Path
from .request import Request
import gzip


def create_write_file(full_path: Path, req: Request):
    try:
        with open(full_path, 'wb') as file:
            file.write(req.body)
        with open(full_path, 'rb') as file_read:
            read_data = file_read.read()
            print(f"Read data from '{full_path}': {read_data}")
        return True
    except OSError as e:
        print(f"An operating system error occured: {e}")
        return False


def handle_request(req: Request, file_root: Path):
    path = req.target
    conn_header = ""
    conn_value = req.get_header("connection")
    if conn_value == "close":
        conn_header = "Connection: close"

    if path.startswith("/echo/"):
        _, _, string = path.partition("/echo/")
        body = string.encode("utf-8")
        if "accept-encoding" in req.headers:
            comp_scheme = req.get_header("accept-encoding")
            if "gzip" not in comp_scheme:
                headers = [HTTP_CODE_200,
                           "Content-Type: text/plain",
                           f"Content-Length: {len(body)}",]
                if conn_header:
                    headers.append(conn_header)
                head = CRLF.join(headers) + END_HEADERS
                return head.encode("utf-8") + body
            else: 
                compressed_body = gzip.compress(body)   
                headers = [HTTP_CODE_200,
                        "Content-Type: text/plain",
                        f"Content-Encoding: gzip",
                        f"Content-Length: {len(compressed_body)}",]
                if conn_header:
                    headers.append(conn_header)
                head = CRLF.join(headers) + END_HEADERS
                return head.encode("utf-8")+compressed_body
        else:
            headers = [HTTP_CODE_200,
                    "Content-Type: text/plain",
                    f"Content-Length: {len(body)}",]
            if conn_header:
                headers.append(conn_header)
            head = CRLF.join(headers) + END_HEADERS
            return head.encode("utf-8") + body
    
    elif path == "/user-agent":
        ua = req.get_header("user-agent")
        body = ua.encode("utf-8")
        headers =[HTTP_CODE_200,
               "Content-Type: text/plain",
               f"Content-Length: {len(body)}",]
        if conn_header:
            headers.append(conn_header)
        head = CRLF.join(headers) + END_HEADERS
        return head.encode('utf-8') + body
    
    elif path.startswith("/files/"):
        _, _, filename = path.partition("/files/")
        if not filename or "/" in filename or ".." in filename:
            head = HTTP_CODE_404 + END_HEADERS
            return head.encode("utf-8")
        else:
            full_root = file_root.resolve()
            full_path = (full_root / filename).resolve()
            try:
                full_path.relative_to(full_root)
            except ValueError:
                print(f"Cannot read '{filename}' "
                      "as it is outside the permitted directory.")
                head = HTTP_CODE_404 + END_HEADERS
                return head.encode("utf-8")
            
            if req.method == 'GET':
                if not full_path.is_file():
                    print(f"'{filename}' is not a file or format not allowed.")
                    head = HTTP_CODE_404 + END_HEADERS
                    return head.encode("utf-8")
                try:
                    content = full_path.read_bytes()
                    headers = [HTTP_CODE_200,
                            "Content-Type: application/octet-stream",
                            f"Content-Length: {len(content)}",]
                    if conn_header:
                        headers.append(conn_header)
                    head = CRLF.join(headers) + END_HEADERS
                    return head.encode('utf-8') + content
                
                except Exception as e:
                    print(f"Error reading {filename}: {str(e)}")
                    head = HTTP_CODE_404 + END_HEADERS
                    return head.encode("utf-8")

            if req.method == 'POST':
                if create_write_file(full_path, req):
                    head = HTTP_CODE_201 + END_HEADERS
                    return head.encode('utf-8')

    elif path == "/":
        body = b""
        headers = [HTTP_CODE_200,                     
                "Content-Type: text/plain",
                "Content-Length: 0",]
        if conn_header:
            headers.append(conn_header)
        head = CRLF.join(headers) + END_HEADERS
        return head.encode("utf-8") + body
    
    else:
        body = b""
        head = (
            CRLF.join([
                HTTP_CODE_404,                     
                "Content-Type: text/plain",
                "Content-Length: 0",
            ]) + END_HEADERS
        )
        return head.encode("utf-8") + body
    