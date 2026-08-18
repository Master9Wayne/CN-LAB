import socket, os

c = socket.socket()
c.connect(('127.0.0.1', 5000))

c.sendall(f"{input('User: ')}|{input('Pass: ')}".encode())

try: 
    if c.recv(1024).decode() == "OK":
        print("Authentication successful.")
        
        while True: 
            cmd = input("\n1. Upload | 2. Download | 3. Exit\nChoice: ")
            
            if cmd == '1':
                fname = input("File to upload: ")
                if os.path.exists(fname):
                    c.sendall(f"UPLOAD|{fname}".encode())
                    with open(fname, "rb") as f: 
                        c.sendall(f.read()) 
                    print("Upload sent.")
                else: 
                    print("File does not exist locally.")
                    
            elif cmd == '2': 
                fname = input("File to download: ")
                c.sendall(f"DOWNLOAD|{fname}".encode())
                res = c.recv(4096)
                if res.startswith(b"OK|"):
                    with open("dl_" + fname, "wb") as f: 
                        f.write(res.split(b'|', 1)[1]) 
                    print("File downloaded successfully.")
                else: 
                    print("Server Error:", res.decode().split('|')[1])
                    
            elif cmd == '3':
                c.sendall(b"EXIT|")
                break
    else: 
        print("Authentication failed.")
except Exception as e:
    print(f"Connection error: {e}")
finally:
    c.close()