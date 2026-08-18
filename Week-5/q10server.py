import socket, threading, datetime, os

users = {"Alice": "alice123", "Bob": "bob123"} 
log_lock = threading.Lock()

def log(u, op, stat): 
    with log_lock, open("activity.log", "a") as f:
        f.write(f"{datetime.datetime.now()} | {u} | {op} | {stat}\n")

def handle_client(c): 
    user = "Unknown"
    try:
        user, pwd = c.recv(1024).decode().split('|')
        if users.get(user) != pwd:
            c.sendall(b"FAIL")
            log(user, "LOGIN", "FAIL")
            return
        
        c.sendall(b"OK")
        log(user, "LOGIN", "OK")
        
        while True: 
            req = c.recv(1024).decode().split('|')
            if not req or req[0] == "EXIT": break
            
            cmd, fname = req[0], req[1]
            if cmd == "UPLOAD":
                with open("srv_" + fname, "wb") as f: 
                    f.write(c.recv(4096))
                log(user, f"UPLOAD {fname}", "OK")
                
            elif cmd == "DOWNLOAD": 
                if os.path.exists("srv_" + fname):
                    with open("srv_" + fname, "rb") as f: 
                        c.sendall(b"OK|" + f.read())
                    log(user, f"DOWNLOAD {fname}", "OK")
                else:
                    c.sendall(b"ERR|File not found")
                    log(user, f"DOWNLOAD {fname}", "FAIL")
                    
    except Exception as e: 
        log(user, "ERROR", str(e)) 
    finally: 
        c.close()

s = socket.socket()
s.bind(('127.0.0.1', 5000))
s.listen()

while True:
    conn, _ = s.accept()
    threading.Thread(target=handle_client, args=(conn,)).start()