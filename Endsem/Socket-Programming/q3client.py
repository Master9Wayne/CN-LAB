import socket # Imports socket module
import time # Imports time module

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Creates UDP socket
client.settimeout(2.0) # Sets a 2-second timeout for blocking operations
server_addr = ('127.0.0.1', 5000) # Defines server address

file_chunks = [b"Chunk1", b"Chunk2", b"Chunk3", b"Chunk4"] # Simulated file chunks
seq_num = 1 # Initializes sequence number

for chunk in file_chunks: # Iterates over all chunks
    packet = f"{seq_num}|".encode() + chunk # Constructs packet: "SEQ|DATA"
    acknowledged = False # Flag to track ACK status
    
    while not acknowledged: # Loop for Stop-and-Wait ARQ
        print(f"Sending SEQ={seq_num}") # Logs sending action
        client.sendto(packet, server_addr) # Sends packet via UDP
        try:
            ack_data, _ = client.recvfrom(1024) # Waits for ACK (blocks up to 2s)
            ack_seq = int(ack_data.decode()) # Extracts ACK sequence number
            if ack_seq == seq_num: # Checks if ACK matches current sequence
                print(f"ACK={ack_seq} received.") # Logs success
                acknowledged = True # Sets flag to break loop and move to next chunk
        except socket.timeout: # Catches timeout exception
            print("Timeout occurred. Retransmitting...") # Logs timeout and reloops
            
    seq_num += 1 # Increments sequence number for next packet

client.close() # Closes UDP socket
