import socket # Imports socket module

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creates TCP socket
client.connect(('127.0.0.1', 5000)) # Connects to quiz server

name = input("Enter your name: ") # Gets participant name
client.sendall(name.encode()) # Sends name to initialize score

print(client.recv(1024).decode(), end="") # Receives and prints the question
ans = input() # Gets answer from user
client.sendall(ans.encode()) # Sends answer to server

print(client.recv(1024).decode()) # Receives correct/incorrect feedback
print(client.recv(1024).decode()) # Receives final score
client.close() # Closes socket