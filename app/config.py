class ServerConfig: 
    def __init__(self,
                 host,
                 port,
                 root_dir,
                 ): 
        self.host = host 
        self.port = port 
        self.root_dir = root_dir
        self.max_headers_bytes = 32_768
        self.max_body_bytes = 10_000_000
        self.max_concurrent_connections = 32
        self.recv_time_out = 5.0
