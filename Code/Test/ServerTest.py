import socket

# Configuration du serveur
host = '127.0.0.1'  # Adresse IP du serveur (localhost)
port = 12345        # Port d'écoute

# Création du socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(1)

print(f"Serveur en attente de connexion sur le port {port}...")

# Accepter une connexion entrante
conn, addr = server_socket.accept()
print(f"Connexion établie avec {addr}")

# Recevoir des données du client
data = conn.recv(1024).decode()
print(f"Données reçues du client : {data}")

# Envoyer une réponse au client
response = f"Message reçu par le serveur: {data}"
conn.send(response.encode())

# Fermer la connexion
conn.close()
server_socket.close()