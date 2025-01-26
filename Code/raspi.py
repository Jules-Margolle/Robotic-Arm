import smbus
import time
import RPi.GPIO as GPIO

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
    data = bus.read_i2c_block_data(ARDUINO_I2C_ADDRESS, 0, 8)
    return data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7]

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
        array_to_send = [0]
        send_array(3, array_to_send)
    
    elif command == "4":
        array_to_send = [0]
        send_array(4, array_to_send)

    elif command == "5":
        array_to_send = [0]
        send_array(5, array_to_send)

    elif command == "6":
        array_to_send = [0]
        send_array(6, array_to_send)
    elif command == "7":
        array_to_send = [0]
        send_array(7, array_to_send)
    elif command == "8":
        array_to_send = [0]
        send_array(8, array_to_send)

"""
    # Une fois les positions enregistrées, envoyez-les à l'Arduino si nécessaire
    if len(positions) > 0:
        send_array(2, [len(positions)])
        for pos in positions:
            tab = [pos[0], pos[1], pos[2], pos[3], pos[4], pos[5], pos[6], pos[7]]
            send_array(40, tab)  # Envoyer chaque position à l'Arduino
            while GPIO.input(REACHED_POSITION) == GPIO.LOW:
                time.sleep(0.1)
            
        positions.clear()  # Réinitialiser le tableau des positions
"""
