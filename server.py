"""
threading library is used to create multiple threads in out program. Threads allow clients
to be served regardless of other clients being finished or not, by separating code out.
"""

import threading
import socket

# first message to the server is the header with the length of 64, which indicates length of all upcoming messages
HEADER = 64

# a safe bet on using an empty port
PORT = 5050

# automatically get local IP address
IP = socket.gethostbyname(socket.gethostname())

# binding IP address and port to be defined for our socket
ADDR = (PORT, IP)

FORMAT = 'utf-8'

"""
Each time the connection is closed, a message should be sent to notify the server that the user is disconnected.
Avoiding this might cause problems when the very same client is establishing a new connection again.
"""
DISCONNECT_MESSAGE = "!DISCONNECT"

# creating a new socket
# AF_NET = type of socket , SOCK_STREAM = utilizing the socket to support data streams
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# binding our socket with PORT and IP
server.bind(ADDR)


# The below function runs for each client concurrently
# Handling threads and passing connections to be handled
def handle_client(conn, addr):

    connected = True
    print(f"[NEW CONNECTION] {addr} connected.")

    while connected:

        # this is a blocking line of code, meaning it will not be passed until a message (msg) is received form clients
        # messaging protocols define how many bytes of data our server socket should expect
        msg_length = conn.recv(HEADER).decode(FORMAT)

        msg_length = int(msg_length)

        # receiving messages
        msg = conn.recv(msg_length).decode(FORMAT)

        # handling if the message is related to disconnection
        if msg == DISCONNECT_MESSAGE:
            connected = False

        # if not, printing the message itself ...
        print(f"[{addr}] {msg}")

    # disconnect when the connection is shut down
    conn.close()


# creating and handling new connections and allowing the server to listen for connections
def start():

    # listening for new connections ...
    server.listen()

    # notifying users about server listening to the connections
    print(f"[LISTENING] Server is listening on {IP}")

    while True:

        # wait for new connections to the server, store their ADDR and accept them with storing an instance object.
        conn, addr = server.accept()

        # target = where should the connectio be passed, args = what arguments of the connection are
        thread = threading.Thread(target=handle_client, args=(conn, addr))

        # start the thread
        thread.start()

        # print the number of active connections
        print(f"f[ACTIVE CONNECTIONS] {threading.active_count() -1}")


print("[STARTING] Server is starting...")
start()
