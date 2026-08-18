import socket # Imports the socket module
import threading # Imports threading to allow simultaneous sending and receiving

def receive_messages(sock): # Function to handle incoming messages
    while True: # Infinite loop to listen for messages
        try:
            message = sock.recv(1024).decode() # Receives and decodes messages from the server
            if not message: # Checks if the connection was closed
                break # Exits the loop
            print(message) # Prints the received message to the console
        except:
            break # Breaks on connection error

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creates a TCP socket
client.connect(('127.0.0.1', 5000)) # Connects to the server

username = input("Enter username: ") # Prompts user for a unique username
client.sendall(username.encode()) # Sends the username to the server

recv_thread = threading.Thread(target=receive_messages, args=(client,)) # Creates a thread for receiving messages
recv_thread.start() # Starts the receiving thread

while True: # Infinite loop for user input
    msg = input() # Takes input from the user
    if msg.lower() == '/quit': # Checks for exit command
        break # Exits the input loop
    client.sendall(msg.encode()) # Sends the message to the server

client.close() # Closes the socket when done