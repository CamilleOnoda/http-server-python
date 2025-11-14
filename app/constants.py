import time

VERSION = time.strftime("build-%H:%M")

HTTP_CODE_200 = "HTTP/1.1 200 OK"
HTTP_CODE_201 = "HTTP/1.1 201 Created"
HTTP_CODE_400 = "HTTP/1.1 400 Bad Request"
HTTP_CODE_404 = "HTTP/1.1 404 Not Found"
HTTP_CODE_408 = "HTTP/1.1 408 Request Timeout"
HTTP_CODE_413 = "HTTP/1.1 413 Payload Too Large"
HTTP_CODE_501 = "HTTP/1.1 501 Not Implemented"

CRLF = "\r\n"
CRLF_BYTES = CRLF.encode("utf-8")

END_HEADERS = "\r\n\r\n"
END_HEADERS_BYTES = END_HEADERS.encode("utf-8")
