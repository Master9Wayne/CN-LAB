import socket # Imports socket module

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Creates UDP socket
server.bind(('127.0.0.1', 5000)) # Binds UDP socket

expected_seq = 1 # Tracks the next sequence number expected
simulate_drop = True # Flag to simulate dropping a specific packet

while True: # Infinite loop to receive packets
    data, addr = server.recvfrom(1024) # Receives UDP packet
    parts = data.split(b'|', 1) # Splits packet into SEQ and DATA
    seq_num, chunk = int(parts[0].decode()), parts[1] # Extracts values
    
    # Packet Loss Simulation
    if seq_num == 2 and simulate_drop: # Simulates dropping packet SEQ=2 once
        print("Packet loss simulation: SEQ=2 deliberately dropped.")
        simulate_drop = False # Resets flag so retransmission succeeds
        continue # Skips sending ACK
        
    if seq_num == expected_seq: # Checks if packet is the expected one in order
        print(f"Received correct packet: SEQ={seq_num}") # Logs success
        # In a real app, write chunk to file here
        expected_seq += 1 # Increments expected sequence
    else:
        print(f"Received duplicate/out-of-order packet: SEQ={seq_num}") # Logs duplicate
        
    ack_packet = str(seq_num).encode() # Creates ACK packet
    server.sendto(ack_packet, addr) # Sends ACK back to client
