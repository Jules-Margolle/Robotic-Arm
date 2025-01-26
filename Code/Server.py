import socket
import smbus
import time
import RPi.GPIO as GPIO

ARDUINO_I2C_ADDRESS = 0x08
bus = smbus.SMBus(1)

host = '192.168.1.17'
port = 12345

def send_array(command, array):
    
    for i in range(0, len(array), 32):
        chunk = array[i:i+32]
        bus.write_i2c_block_data(ARDUINO_I2C_ADDRESS, command, chunk)  
        time.sleep(0.1)

def read_feedback():
    data = bus.read_i2c_block_data(ARDUINO_I2C_ADDRESS, 0, 8)
    return data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7]


def data_handler(data):
    array_to_send = [0]
    send_array(int(data), array_to_send)


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

