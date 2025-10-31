🧩 Build Your Own HTTP Server (Python)

This project is part of the Codecrafters: "Build Your Own HTTP Server" challenge.
It is written in Python 3 and built entirely from scratch using sockets, no external frameworks.

- Features implemented so far

	- TCP server setup: handles incoming socket connections.
	- Basic HTTP request parsing: extracts method, path, and headers
	- Echo endpoint (/echo/<string>) – returns text sent in the path
	- User-Agent endpoint (/user-agent) – returns client’s User-Agent header
	- Concurrent connections – handles multiple clients at once using threads
	- Implemented with a semaphore to limit simultaneous threads
	- Added logging safeguards (Lock, flush=True) to keep output readable
	- Graceful connection handling – proper socket closure and timeout management

- Key learnings

	- How HTTP/1.1 requests and responses are structured
	- Difference between concurrent and sequential handling
	- Practical use of Python’s threading, Lock, and Semaphore
	- Why daemon threads are convenient for testing but not for production
	- How curl behavior can vary depending on connection headers and timing

- Tech stack

	- Language: Python 3
	- Modules: socket, threading
	- Testing: manual with curl and automated Codecrafters tests

- Next steps

	- File server endpoint (/files/<filename>) – serves files from a directory passed with --directory
	- Implement POST file upload
	- Add Content-Encoding (gzip) support
	- Improve error handling and logging structure
