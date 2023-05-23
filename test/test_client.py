import unittest
import socket
import threading
import sys
import time

from unittest.mock import patch
from sockets.client import send, DISCONNECT_MESSAGE


class SendTestCase(unittest.TestCase):

    def setUp(self):
        # Set up the client sockets for testing
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.bind(('localhost', 0))
        self.client_socket.listen(1)
        self.client_addr = self.client_socket.getsockname()

    def tearDown(self):
        # Close the client sockets after each test
        self.client_socket.close()

    def test_send(self):
        # Mock the client connection
        with patch('sockets.sockets') as mock_socket:
            mock_socket.return_value = self.client_socket

            # Start the server in a separate thread
            thread = threading.Thread(target=send, args=(self.client_addr,))
            thread.start()
            time.sleep(0.1)

            # Call the send function
            send("Test message")

            # Wait for the server to receive and send the response
            time.sleep(0.1)

            # Check if the message was sent correctly
            self.assertEqual(sys.stdout.getvalue(), "Test message\n")

            # Stop the server thread
            self.client_socket.sendall(DISCONNECT_MESSAGE.encode())
            thread.join()


if __name__ == '__main__':
    unittest.main()
