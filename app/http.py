from codecs import decode
from .constants import CRLF


def extract_url_path(raw_request):
    text = raw_request.decode('utf-8', errors='replace')
    request_line = text.split(CRLF, 1)[0]
    parts = request_line.split(" ", 2)
    if len(parts) != 3:
        raise ValueError("Malformed request line."
                         "Example: 'GET /index.html HTTP/1.1\r\n'")
    return parts[1]