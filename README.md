🧩 Build Your Own HTTP Server (Python)

This project is part of the Codecrafters: "Build Your Own HTTP Server" challenge.
It is written in Python 3 and built entirely from scratch using sockets, no external frameworks.

- Features implemented

	-TCP server setup: accepts and manages incoming socket connections.

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


- Project structure

app/
 ├── server.py    # Main TCP server loop and connection handling
 ├── request.py   # HTTP request parsing (method, path, headers, body)
 ├── http.py      # Builds and sends HTTP responses
 ├── config.py    # Server configuration (timeouts, directories, etc.)
 ├── constants.py # Shared constants (CRLF, status codes, etc.)
 ├── main.py      # Entrypoint to the Server and config flow


- Key learnings

	- The full anatomy of HTTP/1.1 requests and responses.

	- How to structure a Request class to separate parsing logic from I/O.

	- Why header normalization (case-insensitive lookup) prevents subtle bugs.

	- How to enforce content integrity using the Content-Length header.

	- Difference between concurrent and sequential handling with Python threads.

	- Practical use of Lock, Semaphore, and socket timeouts for stability.

	- Why daemon threads are convenient for tests but risky in production.


- Tech stack

	- Language: Python 3

	- Core modules: socket, threading, pathlib, dataclasses

	- Testing: manual with curl, unittest and automated Codecrafters tests

- Next steps

	- Implement Transfer-Encoding: chunked for streamed bodies.

	- Add persistent connections (HTTP/1.1 Keep-Alive).

	- Support Content-Encoding (gzip) for compression.

	- Improve structured logging and error output.
