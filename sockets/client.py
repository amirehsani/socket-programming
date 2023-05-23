import socket

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
IP = socket.gethostbyname(socket.gethostname())
ADDR = (IP, PORT)

# creating the client side of the sockets
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
client.setblocking(False)  # Set socket to non-blocking mode


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)


while True:
    packet = input()

    if packet != 'disconnect':
        send(packet)

    else:
        send(DISCONNECT_MESSAGE)
        break

    try:
        response = client.recv(2048).decode(FORMAT)
        if response:
            print(response)
    except socket.error:
        pass
