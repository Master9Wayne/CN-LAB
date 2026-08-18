import socket # Imports socket module

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creates TCP client socket
client.connect(('127.0.0.1', 5000)) # Connects to the server

number = input("Enter an integer: ") # Gets integer input from user
client.sendall(number.encode()) # Sends the encoded number to the server

response = client.recv(1024).decode() # Receives the factorial result
print("Server Response:\n" + response) # Prints the result

client.close() # Closes the client socket