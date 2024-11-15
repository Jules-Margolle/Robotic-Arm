import socket
import threading

def handle_client(conn, addr):
    print(f"New connexion established with {addr}")
    data = conn.recv(1024).decode()
    print(f"Message from client : {data}")
    welcome_message = "Hello from Server\n"
    conn.send(welcome_message.encode())
    
    while data != "close":
        data = conn.recv(1024).decode()
        print(f"Data from {addr} : {data}")

        response = "Message received from SERVER\n"
        conn.send(response.encode())
    
    print(f"Closing connection with {addr}")
    conn.close()

def main(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Server is listening on port {port}")

    while True:
        conn, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()

        
