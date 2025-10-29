from dataclasses import dataclass, field
from operator import contains
from typing import Optional, Dict, Tuple
from .constants import CRLF, CRLF_BYTES, END_HEADERS, HTTP_CODE_400


class BadRequest(Exception):
    pass


class NotImplementedTE(Exception):
    pass


@dataclass
class Request:
    method: str
    target: str
    http_version: str
    headers: Dict[str, str]
    content_length: Optional[int]
    transfer_encoding: Optional[str]
    connection: Optional[str]
    body_prefix: bytes = field(default_factory=bytes)
    body: Optional[bytes] = None
    remote_addr: Optional[Tuple[str,int]] = None


    @classmethod
    def create_request_instance(cls,
                                header_bytes,
                                body_prefix,
                                remote_addr: Optional[Tuple[str,int]]
                                ) -> "Request":
        """Classmethod that parses raw bytes into a Request instance"""

        text = header_bytes.decode("utf-8",errors="replace")

        try:
            start_line, header_block = text.split(CRLF,1)
        except ValueError:
            raise BadRequest("Malformed request: missing CRLF after the start-line")
        
        parts = start_line.split(" ")
        if len(parts) != 3:
            raise BadRequest("Malformed request line: "
                             "single space, request-target, another single space,"
                             "protocol version, and ends with CRLF")
        method, target, http_version = parts[0], parts[1], parts[2]

        headers: dict[str,str] = {}
        for line in header_block.split(CRLF):
            if not line:
                continue
            name, sep, value = line.partition(":")
            if not sep:
                raise BadRequest("Malformed header line (missing ':')")
            headers[name.strip()] = value.strip()

        te = headers.get("transfer-encoding")
        if te:
            if "chunked" in te.lower():
                raise NotImplementedTE("Transfer-Encoding: chunked not yet supported")
            
        cl_raw = headers.get("content-length")
        content_length: Optional[int] = None
        if cl_raw is not None:
            try:
                content_length = int(cl_raw)
                if content_length < 0:
                    raise ValueError
            except ValueError:
                raise BadRequest("Invalid Content-Length")

        connection = headers.get("connection")

        return cls(method=method,
                   target=target,
                   http_version=http_version,
                   headers=headers,
                   content_length=content_length,
                   transfer_encoding=te.lower() if te else None,
                   connection=connection.lower() if connection else None,
                   body_prefix=body_prefix,
                   body=None,
                   remote_addr=remote_addr,
                   )
        

    def get_header(self,name):
        """Case-insensitive loopup for a specific header"""
        return self.headers.get(name.lower())
    
    def read_body(self):
        """Should the server be reading the body at all?\n
        Used by 'handle_client' to decide if 
        it should call '_read_request_body()'
        """
        return (self.content_length) > 0
    
    def add_body(self, body: bytes):
        """Safety check to ensure the exact number of bytes are read.\n
        Then set the final body"""
        if (self.content_length) != len(body):
            raise BadRequest("Body length and 'Content-Length' do not match")
        self.body = body



