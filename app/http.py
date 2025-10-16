from .constants import CRLF, END_HEADERS, HTTP_CODE_200, HTTP_CODE_404


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


def handle_request(url_path: str, user_agent: str=""):
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
    



