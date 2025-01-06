import smbus
import time

# Adresse I2C de l'Arduino
ARDUINO_I2C_ADDRESS = 0x08

# Initialiser le bus I2C
bus = smbus.SMBus(1)

def set_servo():
    
    angle = input("Entrez l'angle :")
    command = 1
    bus.write_i2c_block_data(ARDUINO_I2C_ADDRESS, command, [angle])


def readFeeback():
    received_data = bus.read_i2c_block_data(ARDUINO_I2C_ADDRESS, 0, 16)
    message = ''.join([chr(byte) for byte in received_data if byte != 0])
    print(message)
   

# Exemple d'utilisation
try:
    while True:

        command = input("Entrez la commande : 1 pour faire bouger servo, 2 pour lire le feedback")

        if command == "1":
            set_servo()
        elif command == "2":
            readFeedback()

    
except KeyboardInterrupt:
    print("Arrêté par l'utilisateur")