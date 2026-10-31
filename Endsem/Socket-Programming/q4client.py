import socket 

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
client.connect(('127.0.0.1', 5000)) 

while True: 
    print("\n1. Calculator\n2. String\n3. File Transfer\n4. Time\n5. Exit") 
    choice = input("Enter choice: ") 
    
    if choice == '1': 
        n1 = input("Num 1: ")
        n2 = input("Num 2: ")
        op = input("Operator (+,-,*,/): ")
        req = f"CALC|{n1}|{n2}|{op}" 
    elif choice == '2': 
        txt = input("String: ")
        op = input("Op (upper/lower/reverse): ")
        req = f"STRING|{txt}|{op}" 
    elif choice == '3': 
        filename = input("Enter filename to request from server: ")
        req = f"FILE|{filename}"
    elif choice == '4': 
        req = "TIME"
    elif choice == '5': 
        client.sendall("EXIT".encode()) 
        break
    else:
        continue 
        
    client.sendall(req.encode()) 
    
    if choice == '3':
        data = client.recv(4096) 
        if data.startswith(b"ERROR:"):
            print("Server Result:", data.decode())
        else:
            save_path = f"downloaded_{filename}"
            with open(save_path, 'wb') as f:
                f.write(data)
            print(f"File saved successfully as: {save_path}")
    else:
        print("Server Result:", client.recv(1024).decode()) 

client.close()
