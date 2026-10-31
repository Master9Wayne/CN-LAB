import socket # Imports socket module
import hashlib # Imports hashlib for SHA-256 calculation
import os # Imports os for file size operations

filename = "sample.pdf" # Defines the file to transfer
filesize = os.path.getsize(filename) # Gets the exact size of the file in bytes

sha256 = hashlib.sha256() # Initializes the SHA-256 hash object
with open(filename, "rb") as f: # Opens file in binary read mode
    while chunk := f.read(4096): # Reads file in chunks of 4096 bytes
        sha256.update(chunk) # Updates the hash with the current chunk
original_hash = sha256.hexdigest() # Finalizes the hash as a hex string

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creates TCP socket
client.connect(('127.0.0.1', 5000)) # Connects to server

metadata = f"{filename}|{filesize}|{original_hash}" # Constructs metadata string
client.sendall(metadata.encode()) # Sends metadata to server
client.recv(1024) # Waits for an ACK from the server before sending binary data

with open(filename, "rb") as f: # Opens file again to send data
    while chunk := f.read(4096): # Reads in chunks
        client.sendall(chunk) # Sends the binary chunk directly

result = client.recv(1024).decode() # Receives verification result from server
print("Server verification:", result) # Prints verification success/failure
client.close() # Closes socket
