import socket

def handle_client(conn, addr):
    print(f"New connexion established with {addr}")
    data = conn.recv(1024).decode()
    print(f"Message from client : {data}")
    welcome_message = "Hello from Server"
    conn.send(welcome_message.encode())
    
    
    while(data != "close"):
    
        data = conn.recv(1024).decode()
        print(f"Data from {addr} : {data}")

        response = f"Message received from SERVER {data}"
        conn.send(response.encode())
    

    conn.close

def main(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Server is listening on port {port}")

    while True:
        conn, addr = server_socket.accept()
        handle_client(conn, addr)

        
