import socket

#region
ip = socket.gethostname() #"192.168.20.12" 
ip = "192.168.1.35"
# ip = "172.21.160.1"
# ip = "122.164.80.233"
port = 5000
#endregion

#region
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((ip, port))
#endregion

print("Connected to server")

#region
while True:
    msg = input(">> ")
    client_socket.send(msg.encode())

    if msg.lower().strip() == "exit":
        client_socket.close()
        break

    response = client_socket.recv(1024)
    print(str(response.decode()))
#endregion

client_socket.close()
print("Connection with server closed")