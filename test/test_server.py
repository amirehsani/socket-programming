import unittest
import threading
import socket
import time
import sys


from io import StringIO
from contextlib import redirect_stdout
from sockets.server import handle_client, start, DISCONNECT_MESSAGE


class WebSocketTestCase(unittest.TestCase):

    def setUp(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', 0))
        self.server_socket.listen(1)
        self.server_addr = self.server_socket.getsockname()

    def tearDown(self):
        # Close the server sockets after each test
        self.server_socket.close()

    def test_handle_client(self):
        # Create a mock client sockets for testing
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(self.server_addr)

        # Create a mock message to send
        message = "Test message"
        message_length = len(message)

        # Start the handle_client function in a separate thread
        thread = threading.Thread(target=handle_client, args=(client_socket, self.server_addr))
        thread.start()

        # Send the message to the server
        client_socket.sendall(str(message_length).encode())
        time.sleep(0.1)
        client_socket.sendall(message.encode())
        time.sleep(0.1)
        client_socket.sendall(DISCONNECT_MESSAGE.encode())
        time.sleep(0.1)

        # Wait for the thread to finish
        thread.join()

        # Check if the message was received correctly
        self.assertEqual(sys.stdout.getvalue(), f"[{self.server_addr}] {message}\n")

    def test_start(self):
        # Redirect the stdout to a StringIO object for capturing the output
        with redirect_stdout(StringIO()) as stdout:
            # Start the server in a separate thread
            thread = threading.Thread(target=start)
            thread.start()
            time.sleep(0.1)

            # Create a mock client sockets and connect to the server
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(self.server_addr)
            time.sleep(0.1)

            # Send a message to the server
            client_socket.sendall(str(len("Test message")).encode())
            time.sleep(0.1)
            client_socket.sendall("Test message".encode())
            time.sleep(0.1)
            client_socket.sendall(DISCONNECT_MESSAGE.encode())
            time.sleep(0.1)

            # Wait for the thread to finish
            thread.join()

        # Check if the server's output was captured correctly
        self.assertEqual(stdout.getvalue(), f"[{self.server_addr}] Test message\n")


if __name__ == '__main__':
    unittest.main()
