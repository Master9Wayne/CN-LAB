import socket 
from datetime import datetime 
import os 

def process_request(request): 
    parts = request.split('|') 
    service = parts[0] 
    
    if service == "CALC": 
        num1, num2, op = float(parts[1]), float(parts[2]), parts[3]
        if op == '+': return str(num1 + num2).encode()
        elif op == '-': return str(num1 - num2).encode()
        elif op == '*': return str(num1 * num2).encode()
        elif op == '/': return str(num1 / num2).encode() if num2 != 0 else b"Error: Div by zero"
        
    elif service == "STRING": 
        text, op = parts[1], parts[2].lower()
        if op == "upper": return text.upper().encode()
        elif op == "lower": return text.lower().encode()
        elif op == "reverse": return text[::-1].encode()
        
    elif service == "TIME": 
        return datetime.now().strftime("%d-%m-%Y %H:%M:%S").encode()
        
    elif service == "FILE": 
        filename = parts[1]
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                return f.read() 
        else:
            return b"ERROR: File not found on server."
            
    return b"Invalid Service" 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind(('127.0.0.1', 5000)) 
server.listen() 

while True: 
    conn, addr = server.accept() 
    while True: 
        req = conn.recv(1024).decode() 
        if not req or req == "EXIT": 
            break
        response = process_request(req) 
        conn.sendall(response) 
    conn.close()
