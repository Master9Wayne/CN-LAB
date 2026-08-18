import socket # Imports the socket module for network communication
import threading # Imports threading to handle multiple clients concurrently

clients = {} # Dictionary to map client sockets to their usernames
lock = threading.Lock() # Lock to synchronize access to the shared 'clients' dictionary

def handle_client(client_socket): # Function to handle individual client communication
    username = client_socket.recv(1024).decode().strip() # Receives and decodes the username
    with lock: # Acquires the lock before modifying shared state
        clients[client_socket] = username # Adds the new client to the dictionary
    
    while True: # Infinite loop to continuously receive messages
        try:
            message = client_socket.recv(1024).decode() # Receives a message from the client
            if not message: # If message is empty, the client disconnected
                break # Exits the loop
            
            broadcast_msg = f"[{username}] {message}" # Formats the message for broadcasting
            with lock: # Acquires lock to safely iterate over clients
                for sock in clients: # Iterates through all connected client sockets
                    if sock != client_socket: # Ensures the sender doesn't receive their own message
                        sock.sendall(broadcast_msg.encode()) # Sends the encoded message
        except:
            break # Breaks loop on error (e.g., sudden disconnect)
            
    with lock: # Acquires lock to safely remove the client
        del clients[client_socket] # Removes the disconnected client from the dictionary
    client_socket.close() # Closes the client socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creates a TCP socket
server.bind(('127.0.0.1', 5000)) # Binds the socket to localhost and port 5000
server.listen() # Puts the socket into listening mode

while True: # Infinite loop to accept incoming connections
    client_sock, addr = server.accept() # Accepts a new client connection
    thread = threading.Thread(target=handle_client, args=(client_sock,)) # Creates a new thread for the client
    thread.start() # Starts the client handler thread   