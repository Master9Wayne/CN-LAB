import socket, sqlite3 #[cite: 3]

conn_db = sqlite3.connect("students.db") #[cite: 3]
conn_db.execute("CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY, name TEXT)") #[cite: 3]
conn_db.commit() #[cite: 3]

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #[cite: 3]
server.bind(('127.0.0.1', 5000)); server.listen() #[cite: 3]

while True: #[cite: 3]
    client_sock, _ = server.accept() #[cite: 3]
    req = client_sock.recv(1024).decode().split('|') #[cite: 3]
    op = req[0] #[cite: 3]
    cursor = conn_db.cursor() #[cite: 3]
    
    try:
        if op == "INSERT": cursor.execute("INSERT INTO students VALUES (?, ?)", (int(req[1]), req[2])); res = "Inserted" #[cite: 3]
        elif op == "SEARCH": cursor.execute("SELECT * FROM students WHERE id = ?", (int(req[1]),)); res = str(cursor.fetchone() or "Not found") #[cite: 3]
        elif op == "UPDATE": cursor.execute("UPDATE students SET name = ? WHERE id = ?", (req[2], int(req[1]))); res = "Updated" if cursor.rowcount else "Not found"
        elif op == "DELETE": cursor.execute("DELETE FROM students WHERE id = ?", (int(req[1]),)); res = "Deleted" if cursor.rowcount else "Not found"
        elif op == "DISPLAY": cursor.execute("SELECT * FROM students"); res = str(cursor.fetchall())
        conn_db.commit() #[cite: 3]
    except Exception as e: res = f"DB Error: {str(e)}" #[cite: 3]
        
    client_sock.sendall(res.encode()); client_sock.close() #[cite: 3]