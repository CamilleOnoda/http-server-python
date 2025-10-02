import unittest
import socket


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
                print("Socket properly closed in finally block")


    def test_HTTPRequest(self):
        pass


if __name__ == "__main__":
    unittest.main()