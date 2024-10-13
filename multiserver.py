import socket as s
import sys
import threading

serversocket = s.socket(s.AF_INET, s.SOCK_STREAM)
serversocket.bind(("", 5000))

serversocket.listen()

print(f"Server started on {s.gethostbyname(s.gethostname())}\nAwaiting connections...\n")

clients = {}  # Store connected clients
emptyserver = True

def handle_client(conn, addr):
    global emptyserver, client_thread
    client_name = conn.recv(1024).decode()
    clients[client_name] = conn
    print(client_name+" has joined the server.")
    emptyserver = False
    while True:
        data = conn.recv(1024).decode()
        if data == "exit":
            conn.close()
            print(client_name+" has left the server")
            del clients[client_name]
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
        elif data == "sharedata":
            print("check -"+str(emptyserver)+str(len(clients)))
        print(client_name +" : "+data)
        msg = "Data received by server : " + str(data)
        conn.send(msg.encode())

while True:
    global client_thread

    print("check -"+str(emptyserver)+str(len(clients)))

    try:
        clientsocket, address = serversocket.accept()
    except OSError:
        serversocket.close()
        sys.exit()
        
    client_thread = threading.Thread(target=handle_client, args=(clientsocket, address))
    client_thread.daemon = True
    client_thread.start()



serversocket.close()
