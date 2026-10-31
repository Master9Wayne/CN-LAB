import socket # Imports socket module
import threading # Imports threading for concurrent clients

scores = {} # Shared dictionary to maintain independent scores for each participant
lock = threading.Lock() # Lock to synchronize access to the scores dictionary

question = "Q1: TCP is connection-oriented? (A) Yes (B) No\nAnswer: " # Quiz question
correct_ans = "A" # Correct answer stored on server

def handle_participant(client_sock): # Thread handler for each participant
    name = client_sock.recv(1024).decode() # Receives participant's name
    with lock: # Synchronizes initialization of score
        scores[name] = 0 
        
    client_sock.sendall(question.encode()) # Sends the question
    answer = client_sock.recv(1024).decode().strip().upper() # Receives and normalizes answer
    
    if answer == correct_ans: # Evaluates answer
        with lock: # Synchronizes score update
            scores[name] += 1 
        client_sock.sendall(b"Correct!\n") # Sends feedback
    else:
        client_sock.sendall(b"Incorrect.\n") # Sends feedback
        
    client_sock.sendall(f"Final Score: {scores[name]}".encode()) # Sends final calculated score
    client_sock.close() # Closes connection

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creates TCP socket
server.bind(('127.0.0.1', 5000)) # Binds socket
server.listen() # Listens for connections

while True: # Accept loop
    client, addr = server.accept() # Accepts client
    threading.Thread(target=handle_participant, args=(client,)).start() # Starts participant thread
