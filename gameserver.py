import socket as s
import sys
import threading

serversocket = s.socket(s.AF_INET, s.SOCK_STREAM)
serversocket.bind(("", 5000))

serversocket.listen()

print(f"Server started on {s.gethostbyname(s.gethostname())}\nAwaiting connections...\n")

clients = {}
client_values = {}
client_values_backup = {}
emptyserver = True

def handle_client(conn, addr):
    global emptyserver, client_thread, client_values_backup, clients, client_values
    client_name = conn.recv(1024).decode()
    clients[client_name] = conn
    print(client_name+" has joined the server.")
    # try:
    #     client_values[client_name] = client_values_backup[client_name]
    # except KeyError:
    #     pass
    emptyserver = False
    while True:
        # clients = client_values = {}
        data = conn.recv(1024).decode()
        data = data.split("*")
        data = data[0]
        print(client_name +" : "+data)
        client_values["*"+str(client_name)] = str(data)+"-!"
        if data == "":
            print(client_name+" has left the server")
            del client_values["*"+str(client_name)]
            del clients[client_name]
            print(client_values)
            conn.send(str(client_values).encode())
            conn.close()
            try:
                client_thread.join()
            except RuntimeError:
                pass
                # serversocket.close()
                # sys.exit()
                
            if not emptyserver and len(clients) == 0:
                end = input("end server? :")
                if end == "yes":
                    serversocket.close()
                    sys.exit()
            break
        conn.send(str(client_values).encode())
        

while True:
    global client_thread

    print("check -"+str(emptyserver)+str(len(clients)))
    client_values_backup = client_values

    try:
        clientsocket, address = serversocket.accept()
    except OSError:
        serversocket.close()
        sys.exit()
        
    client_thread = threading.Thread(target=handle_client, args=(clientsocket, address))
    client_thread.daemon = True
    client_thread.start()
