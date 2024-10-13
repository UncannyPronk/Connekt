import socket

# Establish connection to server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 5000))

# Send client name to server
name = input("Enter your name: ")
s.send(name.encode())

while True:
    # Send message to server
    message = input('Me: ')
    s.send(message.encode())

    # Quit chat
    if message == 'exit':
        s.close()
        break

    # Read incoming message
    message = s.recv(1024).decode()
    print(message)
