import socket
import time





host = '127.0.0.1'
port = 8585






def data_handler(data):
    print(f"Message reçu : {data}")


def handle_client(client_socket, client_address):
    print(f"Nouveau client connecté : {client_address}")

    try:
        while True:

            data = client_socket.recv(1024)
            if data:
                print(f"Message reçu : {data.decode('utf-8')}")
                data_handler(data.decode('utf-8'))

    except (ConnectionResetError, BrokenPipeError):
        print("Déconnexion du client")
    finally:
        client_socket.close()


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen(1)

        while True:
            try:
                client_socket, client_address = server_socket.accept()
                handle_client(client_socket, client_address)
            except KeyboardInterrupt:
                print("Serveur arrêté par l'utilisateur")
                break
            except Exception as e:
                print(f"[ERROR] Erreur innatendue : {e}")

start_server()

