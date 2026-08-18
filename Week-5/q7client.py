import socket

# Configuration matching the server
HOST = '127.0.0.1'
PORT = 5000

# Create TCP socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to the server
    client.connect((HOST, PORT))
    print(f"Connected to server at {HOST}:{PORT}")
    
    while True:
        # Get input from the user
        message = input("Enter message (or 'quit' to exit): ")
        
        if message.lower() == 'quit':
            break
            
        # Send message to the server
        client.sendall(message.encode())
        
        # Wait for and print the server's response
        response = client.recv(1024).decode()
        if not response:
            print("Server closed the connection.")
            break
            
        print(f"Reply: {response}")

except ConnectionRefusedError:
    print("Connection refused. Make sure the server is running.")
finally:
    # Always close the socket to clean up
    print("Closing connection.")
    client.close()