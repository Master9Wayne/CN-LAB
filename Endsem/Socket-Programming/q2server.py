import socket # Imports socket module
import threading # Imports threading for concurrent client handling
import math # Imports math module for the factorial calculation

def handle_client(client_socket): # Handler function for each client
    try:
        data = client_socket.recv(1024).decode() # Receives string data from client
        number = int(data) # Converts the received string to an integer
        if number < 0: # Checks for negative input
            result = "Error: Negative input" # Sets error message
        else:
            result = f"Factorial of {number} = {math.factorial(number)}" # Calculates factorial
        client_socket.sendall(result.encode()) # Sends the result back to the client
    except ValueError: # Catches non-integer inputs
        client_socket.sendall(b"Error: Invalid integer") # Sends error message
    finally:
        client_socket.close() # Closes the client connection safely

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creates TCP server socket
server.bind(('127.0.0.1', 5000)) # Binds to address and port
server.listen() # Starts listening for connections

while True: # Main accept loop
    client_sock, addr = server.accept() # Accepts a new connection
    thread = threading.Thread(target=handle_client, args=(client_sock,)) # Creates handler thread
    thread.start() # Starts the thread