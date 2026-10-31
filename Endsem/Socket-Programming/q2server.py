import socket # Imports socket module
import hashlib # Imports hashlib for SHA-256 calculation

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creates TCP socket
server.bind(('127.0.0.1', 5000)) # Binds socket
server.listen() # Listens for connections

client_sock, addr = server.accept() # Accepts client connection
metadata = client_sock.recv(1024).decode().split('|') # Receives and splits metadata
filename, expected_size, original_hash = metadata[0], int(metadata[1]), metadata[2] # Extracts fields

client_sock.sendall(b"ACK") # Sends ACK to start file transfer

received_size = 0 # Initializes received byte counter
with open("received_" + filename, "wb") as f: # Opens new file in binary write mode
    while received_size < expected_size: # Loops until expected bytes are received
        chunk = client_sock.recv(4096) # Receives binary chunk
        f.write(chunk) # Writes chunk to disk
        received_size += len(chunk) # Increments the counter

sha256 = hashlib.sha256() # Initializes new hash object
with open("received_" + filename, "rb") as f: # Opens the received file
    while chunk := f.read(4096): # Reads in chunks
        sha256.update(chunk) # Updates hash
received_hash = sha256.hexdigest() # Finalizes received hash

if received_hash == original_hash: # Compares the two hashes
    client_sock.sendall(b"SHA-256 verification successful.") # Sends success message
else:
    client_sock.sendall(b"SHA-256 verification FAILED.") # Sends failure message

client_sock.close() # Closes client connection
