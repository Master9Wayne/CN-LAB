import socket #[cite: 4]

while True:
    print("\n1. Insert | 2. Search | 3. Update | 4. Delete | 5. Display | 6. Exit") #[cite: 4]
    choice = input("Choice: ") #[cite: 4]
    
    if choice == '1': req = f"INSERT|{input('ID: ')}|{input('Name: ')}" #[cite: 4]
    elif choice == '2': req = f"SEARCH|{input('ID: ')}" #[cite: 4]
    elif choice == '3': req = f"UPDATE|{input('ID: ')}|{input('New Name: ')}"
    elif choice == '4': req = f"DELETE|{input('ID: ')}"
    elif choice == '5': req = "DISPLAY|"
    elif choice == '6': break
    else: continue

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #[cite: 4]
    client.connect(('127.0.0.1', 5000)) #[cite: 4]
    client.sendall(req.encode()) #[cite: 4]
    print("Response:", client.recv(4096).decode()) #[cite: 4]
    client.close() #[cite: 4]