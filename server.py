import socket

#region
# ip = socket.gethostname() #"192.168.20.12"
# ip = "172.21.160.1"
# ip = "122.164.80.233"
port = 5000
#endregion

#region
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("", port))
server_socket.listen(1)
#endregion

print("Server started on "+ socket.gethostbyname(socket.gethostname()) +". Awaiting connection...")

#region
client_socket, address = server_socket.accept()
print("Client connected - " + str(address))

while True:
    data = client_socket.recv(1024)
    if data.decode().lower().strip() == "exit":
        client_socket.close()
        break
    print("Client : " + str(data.decode()))
    msg = "Data received by server : " + str(data.decode())
    client_socket.send(msg.encode())
#endregion

server_socket.close()
print("connection with client closed")