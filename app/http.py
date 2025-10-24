from .constants import CRLF, END_HEADERS, HTTP_CODE_200, HTTP_CODE_404
from pathlib import Path


def get_url(raw_request: bytes):
    text = raw_request.decode('utf-8', errors='replace')
    request_line = text.split(CRLF, 1)[0]
    url_path = request_line.split(" ", 2)
    if len(url_path) != 3:
        raise ValueError("Malformed request line."
                         "Example: 'GET /index.html HTTP/1.1\r\n'")
    return url_path[1]


def parse_headers(raw_request: bytes):
    text = raw_request.decode("utf-8", errors="replace")
    http_request, _, _ = text.partition(END_HEADERS)
    lines = http_request.split(CRLF)
    headers: dict[str,str] = {}
    for line in lines[1:]:
        if not line:
            continue
        name, sep, value = line.partition(":")
        if sep:
            headers[name.strip()] = value.strip()
    return headers


def get_header(raw_request: bytes, name: str):
    headers = parse_headers(raw_request)
    for key, value in headers.items():
        if key.lower() == name.lower():
            return value
    return None


def handle_request(url_path: str, file_root, user_agent: str="", ):
    if url_path.startswith("/echo/"):
        _, _, string = url_path.partition("/echo/")
        body = string.encode("utf-8")
        head = CRLF.join([
            HTTP_CODE_200,
            "Content-Type: text/plain", 
            f"Content-Length: {len(body)}",
            "Connection: close",
            ]) + END_HEADERS
        return head.encode("utf-8") + body
    

    elif url_path == "/user-agent":
        body = user_agent.encode("utf-8")
        head = CRLF.join([
            HTTP_CODE_200,
            "Content-Type: text/plain",
            f"Content-Length: {len(body)}",
            "Connection: close",
            ]) + END_HEADERS
        return head.encode('utf-8') + body
    

    elif url_path.startswith("/files/"):
        _,_,file = url_path.partition("/files/")
        if not file or "/" in file or ".." in file:
            head = HTTP_CODE_404 + END_HEADERS
            return head.encode("utf-8")
        else:
            full_path = (file_root / file).resolve()

            try:
                full_path.relative_to(file_root)
            except ValueError:
                print(f"Cannot read '{file}' as it is outside the permitted directory.")
                head = HTTP_CODE_404 + END_HEADERS
                return head.encode("utf-8")
            
            if not full_path.is_file():
                print(f"'{file}' is not a file or format not allowed.")
                head = HTTP_CODE_404 + END_HEADERS
                return head.encode("utf-8")
            
            try:
                content = full_path.read_bytes()
            except Exception as e:
                print(f"Error reading {file}: {e}")
                head = HTTP_CODE_404 + END_HEADERS
                return head.encode("utf-8")

            head = CRLF.join([
                HTTP_CODE_200,
                "Content-Type: application/octet-stream",
                f"Content-Length: {len(content)}",
                "Connection: close",
                ]) + END_HEADERS
            return head.encode('utf-8') + content

    elif url_path == "/":
        body = b""
        head = (
            CRLF.join([
                HTTP_CODE_200,                     
                "Content-Type: text/plain",
                "Content-Length: 0",
                "Connection: close",
            ]) + END_HEADERS
        )
        return head.encode("utf-8") + body
    

    else:
        body = b""
        head = (
            CRLF.join([
                HTTP_CODE_404,                     
                "Content-Type: text/plain",
                "Content-Length: 0",
                "Connection: close",
            ]) + END_HEADERS
        )
        return head.encode("utf-8") + body
    



