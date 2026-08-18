import socket # Imports socket module
import select # Imports select for I/O multiplexing

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creates TCP socket
server.bind(('127.0.0.1', 5000)) # Binds socket
server.listen() # Listens for connections

sockets_list = [server] # List of sockets to monitor, initialized with the server socket

print("Server started. Waiting for connections...")
while True: # Event loop
    # select() blocks until one or more sockets in sockets_list are ready for reading
    read_sockets, _, _ = select.select(sockets_list, [], []) 
    
    for notified_socket in read_sockets: # Iterates through ready sockets
        if notified_socket == server: # If the ready socket is the server socket
            client_socket, client_address = server.accept() # Accept the new connection
            sockets_list.append(client_socket) # Add new client to monitored list
            print(f"Accepted new connection from {client_address}")
        else: # If the ready socket is a client socket
            try:
                message = notified_socket.recv(1024) # Receive data from client
                if not message: # If empty data, client disconnected
                    sockets_list.remove(notified_socket) # Remove from monitored list
                    notified_socket.close() # Close socket
                    continue
                # Process and send response
                notified_socket.sendall(b"Server: Message received") 
            except: # Handles unexpected client drops
                sockets_list.remove(notified_socket) # Clean up
                notified_socket.close() # Clean up