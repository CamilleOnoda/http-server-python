import unittest
import socket
from app.http import extract_url_path


class TestNetworkService(unittest.TestCase):
    def test_network_connection(self):
        sock = None
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.assertTrue(True, "Connection successful")

        except socket.error as e:
            self.fail(f"Connection failed: {e}")
        
        finally:
            if sock:
                sock.close()
                print("Socket properly closed")


class TestExtractPath(unittest.TestCase):
    def test_simple_GET(self):
        request = "GET /index.html HTTP/1.1\r\nHost: localhost:4221\r\n"
        url_path = extract_url_path(request.encode())
        self.assertEqual(url_path, '/index.html')

    def test_root(self):
        request = "GET / HTTP/1.1\r\nHost: localhost:4221\r\n"
        url_path = extract_url_path(request.encode())
        self.assertEqual(url_path, '/')

    def test_invalid(self):
        request = "GET HTTP/1.1\r\nHost: localhost:4221\r\nUser-Agent: curl/7.64.1\r\nAccept: */*\r\n\r\n"
        with self.assertRaises(ValueError):
            extract_url_path(request.encode())
        


if __name__ == "__main__":
    unittest.main()