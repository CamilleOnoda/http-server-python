from codecs import decode
from .constants import CRLF


def extract_url_path(request_target):
    decoded_request = request_target.decode('utf-8', errors='replace')
    request_line = decoded_request.split(CRLF)[0]
    parts = request_line.split(" ")
    if len(parts) != 3:
        raise ValueError("Malformed request line."
                         "Example: 'GET /index.html HTTP/1.1\r\n'")
    return parts[1]