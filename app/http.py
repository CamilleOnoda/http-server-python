from .constants import CRLF, END_HEADERS, HTTP_CODE_200, HTTP_CODE_404


def extract_url_path(raw_request: bytes):
    text = raw_request.decode('utf-8', errors='replace')
    request_line = text.split(CRLF, 1)[0]
    parts = request_line.split(" ", 2)
    if len(parts) != 3:
        raise ValueError("Malformed request line."
                         "Example: 'GET /index.html HTTP/1.1\r\n'")
    return parts[1]


def handle_request(url_path: str):
    if url_path.startswith("/echo/"):
        _, _, string = url_path.partition("/echo/")

        body = string.encode("utf-8")
        response_headers = CRLF.join([
            f"{HTTP_CODE_200}",
            "Content-Type: text/plain", 
            f"Content-Length: {len(string.encode('utf-8'))}"
            ]) + END_HEADERS
#        response_body = CRLF.join(response_headers).encode("utf-8") + END_HEADERS.encode("utf-8") + body
        return response_headers.encode("utf-8") + body
    elif url_path == "/":
        body = b""
        response_headers = (
            CRLF.join([
                HTTP_CODE_200,                     
                "Content-Type: text/plain",
                "Content-Length: 0",
            ]) + END_HEADERS
        )
        return response_headers.encode("utf-8") + body
    else:
        body = b""
        response_headers = (
            CRLF.join([
                HTTP_CODE_404,                     
                "Content-Type: text/plain",
                "Content-Length: 0",
            ]) + END_HEADERS
        )
        return response_headers.encode("utf-8") + body
    



