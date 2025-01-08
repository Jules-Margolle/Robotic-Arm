import smbus
import time

# Adresse I2C de l'Arduino
ARDUINO_I2C_ADDRESS = 0x08

# Créer une instance de bus
bus = smbus.SMBus(1)  # 1 pour Raspberry Pi récente (I2C-1)

# Tableau pour stocker les positions
positions = []

def send_array(command, array):
    # Découper le tableau en tranches de 32 octets (limite I2C)
    for i in range(0, len(array), 32):
        chunk = array[i:i+32]
        bus.write_i2c_block_data(ARDUINO_I2C_ADDRESS, command, chunk) # 1 est la commande, peut être modifié selon la commande 
        time.sleep(0.1)  # Pause pour éviter les surcharges

def get_positions_to_send():
    pos_axe1 = input("Entrez la position de l'axe 1 : ")
    pos_axe2 = input("Entrez la position de l'axe 2 : ")

    return [int(pos_axe1), int(pos_axe2)]

def read_feedback():
    data = bus.read_i2c_block_data(ARDUINO_I2C_ADDRESS, 0, 2)
    return data[0], data[1]

def record_positions():
    print("Appuyez sur 1 pour enregistrer une position.")
    while True:
        command = input("Entrez '1' pour enregistrer une position ou 'q' pour quitter : ")
        if command == "1":
            pos = read_feedback()
            positions.append(pos)
            print("Position enregistrée :", pos)
        elif command == "q":
            print("Fin de l'enregistrement.")
            break

while True:
    command = input("Entrez la commande : 1 pour faire bouger les servos, 2 pour lire les feedbacks, 3 pour enregistrer des positions : ")

    if command == "1":
        array_to_send = get_positions_to_send()
        send_array(0, array_to_send)
        print("Tableau envoyé :", array_to_send)

    elif command == "2":
        array_to_send = [0]
        send_array(1, array_to_send)
        feedback_array = read_feedback()
        print("Tableau reçu :", feedback_array)

    elif command == "3":
        record_positions()

    # Une fois les positions enregistrées, envoyez-les à l'Arduino si nécessaire
    if len(positions) > 0:
        send_array(2, [len(positions)])  # Indiquer à l'Arduino qu'il y a des positions à charger
        for pos in positions:
            send_array(3, pos)  # Envoyer chaque position à l'Arduino
        positions.clear()  # Réinitialiser le tableau des positions
