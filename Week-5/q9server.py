import socket # Imports socket module
import subprocess # Imports subprocess to execute OS commands safely

allowed_cmds = {"pwd": ["pwd"], "date": ["date"], "ls": ["ls"]} # Strict allowlist of commands

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creates TCP socket
server.bind(('127.0.0.1', 5000)) # Binds socket
server.listen() # Listens for connections

while True: # Main loop
    client, addr = server.accept() # Accepts client
    cmd = client.recv(1024).decode().strip() # Receives and strips command string
    
    if cmd in allowed_cmds: # Security Validation: Checks if command is in allowlist
        try:
            # Executes command safely (sequence format, no shell=True) and captures output/errors
            result = subprocess.run(allowed_cmds[cmd], capture_output=True, text=True, timeout=5)
            # Returns stdout if successful, else returns stderr
            output = result.stdout if result.returncode == 0 else result.stderr 
        except Exception as e:
            output = f"Execution Error: {str(e)}" # Catches internal execution errors
    else:
        output = "Error: Command not permitted." # Rejects un-allowlisted commands
        
    client.sendall(output.encode()) # Sends output back to client
    client.close() # Closes connection