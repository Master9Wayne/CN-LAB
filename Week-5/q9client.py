import socket # Imports socket module

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creates TCP socket
client.connect(('127.0.0.1', 5000)) # Connects to server

cmd = input("Enter command (pwd/date/ls): ") # Prompts user for command
client.sendall(cmd.encode()) # Sends command to server

print("Server output:\n", client.recv(4096).decode()) # Prints the executed output from server
client.close() # Closes connection