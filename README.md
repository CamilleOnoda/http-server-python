🧩 HTTP server from scratch in Python

This project is written in Python 3 and built entirely from scratch using sockets, no external frameworks.

### Features implemented

- TCP server setup: accepts and manages incoming socket connections.
- Basic HTTP request parsing: extracts method, path, and headers.
- Request body handling: reads bodies accurately using the Content-Length header, with timeout and error safeguards.
- File endpoints:
	- /files/{filename} – serves files for GET requests from the directory passed via --directory.
	- POST /files/{filename} – creates or overwrites files by writing the request body to disk.
- Error responses: returns proper HTTP codes (400, 408, 413, 501) for malformed, incomplete, or oversized requests.
- User-Agent endpoint (/user-agent): returns the client’s User-Agent header.
- Echo endpoint (/echo/{string}): returns the text sent in the path.
- Concurrency: handles multiple clients simultaneously with threads, using a semaphore to limit connections.
- Logging and thread safety: uses Lock and flush=True to keep console output readable and consistent.
- Graceful connection handling: proper socket closure and timeouts for robustness.


### Installation
Make sure you have Python 3x installed.

```
# Clone the repo
git clone https://github.com/CamilleOnoda/http-server-python
cd http-server-python

# Run the server
python3 app/main.py --directory ./public
```

### What’s happening behind the scenes

When you start the program, your computer opens a listening socket (like a receptionist waiting for phone calls).
When another program (like your browser or a command such as curl) sends a request, the server reads that message, figures out what’s being asked for, and sends back a reply that follows the rules of the HTTP protocol

For example:
```
curl http://localhost:4221/echo/hello
```
The server reads that request and responds:
```
HTTP/1.1 200 OK
hello
```
In simple terms:

- The server = your program waiting and responding.
- The client = your browser or command line sending messages.
- HTTP = the “language” both sides speak to exchange text and files.

### Project structure
```
app/
 ├── server.py    # Main TCP server loop and connection handling
 ├── request.py   # HTTP request parsing (method, path, headers, body)
 ├── http.py      # Builds and sends HTTP responses
 ├── config.py    # Server configuration (timeouts, directories, etc.)
 ├── constants.py # Shared constants (CRLF, status codes, etc.)
 ├── main.py      # Entrypoint to the Server and config flow
```

### Key learnings
- The full anatomy of HTTP/1.1 requests and responses.
- How to structure a Request class to separate parsing logic from I/O.
- Why header normalization (case-insensitive lookup) prevents subtle bugs.
- How to enforce content integrity using the Content-Length header.
- Difference between concurrent and sequential handling with Python threads.
- Practical use of Lock, Semaphore, and socket timeouts for stability.
- Why daemon threads are convenient for tests but risky in production.

### Tech stack
- Language: Python 3
- Core modules: socket, threading, pathlib, dataclasses
- Testing: manual with curl, unittest and automated Codecrafters tests

### Next steps
- Implement Transfer-Encoding: chunked for streamed bodies.
- Add persistent connections (HTTP/1.1 Keep-Alive).
- Support Content-Encoding (gzip) for compression.
- Improve structured logging and error output.
