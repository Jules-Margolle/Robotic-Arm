import smbus
import time

import numpy as np
import math
from scipy.optimize import fsolve

#Adresse I2C de l'Arduino
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



def compute_rotation_matrix(yaw, pitch, roll):
    """
    Construit la matrice de rotation 3x3 à partir des angles d'Euler (yaw, pitch, roll).
    Les rotations sont effectuées dans l'ordre Z (yaw), Y (pitch), X (roll).
    
    :param yaw: Rotation autour de l'axe Z (en radians)
    :param pitch: Rotation autour de l'axe Y (en radians)
    :param roll: Rotation autour de l'axe X (en radians)
    :return: Matrice de rotation 3x3
    """
    Rz = np.array([[np.cos(yaw), -np.sin(yaw), 0],
                   [np.sin(yaw),  np.cos(yaw), 0],
                   [0,            0,           1]])
    
    Rz2 = np.array([[np.cos(roll), -np.sin(roll), 0],
                   [np.sin(roll),  np.cos(roll), 0],
                   [0,            0,           1]])

    
    Ry = np.array([[np.cos(pitch), 0, np.sin(pitch)],
                   [0,             1, 0],
                   [-np.sin(pitch),0, np.cos(pitch)]])
    
    Rx = np.array([[1, 0,            0],
                   [0, np.cos(roll), -np.sin(roll)],
                   [0, np.sin(roll),  np.cos(roll)]])
    

    
    return Rz @ Ry @ Rz2

def compute_wrist_position_from_angle(theta1, theta2, theta3):
    """
    Calcule la position du poignet à partir des 3 premiers angles du robot.
    
    Ces équations utilisent les paramètres géométriques du robot.
    
    :param theta1: Angle (en degrés) autour de l'axe vertical.
    :param theta2: Angle (en degrés) du joint 2.
    :param theta3: Angle (en degrés) du joint 3.
    :return: Vecteur numpy [X_w, Y_w, Z_w] représentant la position du poignet
    """
    # Conversion en radians
    theta1_rad = np.radians(theta1)
    theta2_rad = np.radians(theta2)
    theta3_rad = np.radians(theta3)
    
    # Paramètres géométriques (exprimés en mm)
    a2 = 190.2
    a3 = 247.6
    d1 = 197.3
    
    X_w = np.cos(theta1_rad) * (a2 * np.sin(theta2_rad) + a3 * np.sin(theta2_rad + theta3_rad))
    Y_w = np.sin(theta1_rad) * (a2 * np.sin(theta2_rad) + a3 * np.sin(theta2_rad + theta3_rad))
    Z_w = d1 + (a2 * np.cos(theta2_rad) + a3 * np.cos(theta2_rad + theta3_rad))
    
    return np.array([X_w, Y_w, Z_w])

def compute_wrist_position(rotation_matrix, position_vector, d6):
    """
    Calcule la position du poignet sphérique à partir de la position de l'effecteur final.
    
    :param rotation_matrix: Matrice de rotation 3x3 de l'effecteur final
    :param position_vector: Vecteur 3x1 représentant la position de l'effecteur final (X, Y, Z)
    :param d6: Décalage entre l'effecteur final et le centre du poignet
    :return: Vecteur 3x1 représentant la position du poignet sphérique (X_w, Y_w, Z_w)
    """
    # Le vecteur Z6 est la troisième colonne de la matrice de rotation
    Z6 = rotation_matrix[:, 2]
    wrist_position = position_vector - d6 * Z6
    return wrist_position

def calculer_position_poignet(wrist_position, pitch, roll, yaw, d=47.998):
    """
    Calcule la position (x, y, z) du poignet sphérique d'un robot.

    Paramètres :
      - final_x, final_y, final_z : Coordonnées de l'effecteur (TCP)
      - pitch, roll, yaw : Angles d'Euler en radians (rotation autour de Y, X et Z respectivement)
      - d : Distance entre le poignet et l'effecteur (le décalage le long de l'axe z de l'outil)

    Retourne :
      - Un tableau numpy [x, y, z] représentant la position du poignet.
    """
    final_x, final_y, final_z = wrist_position
    # Matrice de rotation pour la rotation autour de l'axe X (roll)
    R_x = np.array([
        [1, 0, 0],
        [0, np.cos(roll), -np.sin(roll)],
        [0, np.sin(roll),  np.cos(roll)]
    ])
    
    # Matrice de rotation pour la rotation autour de l'axe Y (pitch)
    R_y = np.array([
        [np.cos(pitch), 0, np.sin(pitch)],
        [0, 1, 0],
        [-np.sin(pitch), 0, np.cos(pitch)]
    ])
    
    # Matrice de rotation pour la rotation autour de l'axe Z (yaw)
    R_z = np.array([
        [np.cos(yaw), -np.sin(yaw), 0],
        [np.sin(yaw),  np.cos(yaw), 0],
        [0, 0, 1]
    ])
    
    # Ordre de rotation : d'abord yaw, puis pitch, enfin roll.
    R = R_z @ R_x @ R_z
    #print(R)

    # Position finale de l'effecteur (TCP)
    p = np.array([final_x, final_y, final_z])
    
    # Vecteur d'offset dans le repère outil (défini le long de l'axe z)
    offset = d * np.array([0, 0, 1])
    
    # Calcul de la position du poignet : on retranche l'offset transformé
    poignet = p - R @ offset
    
    return poignet

def calculer_angles(wrist, theta1_deg):
    """
    Calcule les angles theta2 et theta3 à partir des coordonnées du poignet.    
    :param wrist: Coordonnées (x, z) du poignet
    :param theta1: Premier angle (déjà calculé) en degrés
    :return: theta2 et theta3 en degrés
    """
    
    a2 = 190.2
    a3 = 247.6
    d1 = 197.3
    
    
    X_w,Y_w,Z_w = wrist
    
    theta1_rad = np.radians(theta1_deg)
    
    # Calcul de r
    r = np.sqrt(X_w**2 + Y_w**2)
    
    # Calcul de theta3
    num = r**2 + (Z_w - d1)**2 - a2**2 - a3**2
    den = 2 * a2 * a3
    cos_theta3 = num / den
    
    # Vérification des valeurs possibles pour éviter des erreurs d'arc cos
    if cos_theta3 < -1 or cos_theta3 > 1:
        print("Impossible de calculer theta3, vérifier les entrées")
    
    theta3_rad = -np.arccos(cos_theta3)  # Solution positive
    
    # Calcul de theta2
    term1 = np.arctan2(Z_w - d1, r)
    term2 = np.arctan2(a3 * np.sin(theta3_rad), a2 + a3 * np.cos(theta3_rad))
    theta2_rad = term1 - term2
    
    # Convertir en degrés
    theta2 = np.degrees(theta2_rad)
    theta3 = np.degrees(theta3_rad)
    
    return -(theta2-90), -theta3

def compute_joint_angles(wrist_position):
    """
    Calcule les angles theta1, theta2, theta3 à partir de la position du poignet.
    :param wrist_position: Vecteur 3x1 (X_w, Y_w, Z_w)
    :return: theta1, theta2, theta3 en degrés
    """
    X_w, Y_w, _ = wrist_position
    
    # Calcul de theta1 (rotation autour de l'axe vertical)
    theta1 = np.degrees(np.arctan2(Y_w, X_w)) % 360
    
    # Pour theta2 et theta3, on travaille dans le plan (X, Z)
    theta2, theta3 = calculer_angles(wrist_position, theta1)
    
    return theta1, theta2, theta3


def compute_R0_3(theta1, theta2, theta3):
    """
    Calcule la matrice de rotation de la base au joint 3
    en supposant :
      - rotation du joint 1 autour de Z
      - rotations des joints 2 et 3 autour de Y
    
    :param theta1: Angle du joint 1 (en degrés)
    :param theta2: Angle du joint 2 (en degrés)
    :param theta3: Angle du joint 3 (en degrés)
    :return: Matrice 3x3 R0_3
    """
    theta1_rad = np.radians(theta1)
    theta2_rad = np.radians(theta2)
    theta3_rad = np.radians(theta3)
    
    Rz = np.array([[np.cos(theta1_rad), -np.sin(theta1_rad), 0],
                   [np.sin(theta1_rad),  np.cos(theta1_rad), 0],
                   [0,                   0,                  1]])
    
    Ry2 = np.array([[np.cos(theta2_rad), 0, np.sin(theta2_rad)],
                    [0,                  1, 0],
                    [-np.sin(theta2_rad),0, np.cos(theta2_rad)]])
    
    Ry3 = np.array([[np.cos(theta3_rad), 0, np.sin(theta3_rad)],
                    [0,                  1, 0],
                    [-np.sin(theta3_rad),0, np.cos(theta3_rad)]])
    
    return Rz @ Ry2 @ Ry3

def compute_wrist_angles(R_6_0, theta1, theta2, theta3,pitch,roll,yaw):
    """
    Calcule les 3 derniers angles (theta4, theta5, theta6) du robot.
    
    La procédure est la suivante :
      1. Calcul de la matrice R0_3 à partir des trois premiers angles.
      2. Calcul de la matrice de rotation résiduelle du poignet : R3_6 = (R0_3)^T * R0_6.
      3. Extraction des angles en supposant que R3_6 se décompose en Rz(theta4) * Ry(theta5) * Rz(theta6).
    
    :param R0_6: Matrice de rotation de l'effecteur final (issue de compute_rotation_matrix)
    :param theta1: Premier angle (en degrés)
    :param theta2: Deuxième angle (en degrés)
    :param theta3: Troisième angle (en degrés)
    :return: theta4, theta5, theta6 en degrés
    """
    
    theta1_rad = np.radians(theta1)
    theta2_rad = np.radians(theta2)
    theta3_rad = np.radians(theta3)
    
 # Calcul de la matrice de rotation de l'effecteur
    # R_roll = np.array([[1, 0, 0], [0, np.cos(np.radians(roll)), -np.sin(np.radians(roll))], [0, np.sin(np.radians(roll)), np.cos(np.radians(roll))]])
    # R_pitch = np.array([[np.cos(np.radians(pitch)), 0, np.sin(np.radians(pitch))], [0, 1, 0], [-np.sin(np.radians(pitch)), 0, np.cos(np.radians(pitch))]])
    # R_yaw = np.array([[np.cos(np.radians(yaw)), -np.sin(np.radians(yaw)), 0], [np.sin(np.radians(yaw)), np.cos(np.radians(yaw)), 0], [0, 0, 1]])
    
    

    
    # Calcul de la matrice de rotation du poignet
    R_3_0 = np.array([[np.cos(theta1_rad) * np.cos(theta2_rad + theta3_rad), -np.cos(theta1_rad) * np.sin(theta2_rad + theta3_rad), np.sin(theta1_rad)],
                       [np.sin(theta1_rad) * np.cos(theta2_rad + theta3_rad), -np.sin(theta1_rad) * np.sin(theta2_rad + theta3_rad), -np.cos(theta1_rad)],
                       [np.sin(theta2_rad + theta3_rad), np.cos(theta2_rad + theta3_rad), 0]])
    
    R_6_3 = np.linalg.inv(R_3_0) @ R_6_0
    
    # Extraction des angles theta4, theta5, theta6
    theta4_rad = np.arctan2(R_6_3[1, 2], R_6_3[0, 2])
    theta5_rad = np.arccos(R_6_3[2, 2])
    theta6_rad = np.arctan2(R_6_3[2, 1], -R_6_3[2, 0])
    
    
    theta4_deg = np.degrees(theta4_rad)
    theta5_deg = np.degrees(theta5_rad)
    theta6_deg = np.degrees(theta6_rad)
    
    theta4_deg = theta4_deg % 360
    theta5_deg = theta5_deg % 360
    theta6_deg = theta6_deg % 360

    
    
    return theta4_deg-90, theta5_deg-90, theta6_deg+90

def in_limite_robot(P_w,theta1,theta2,theta3):
    """
    Vérifie si un point est dans la zone de travail du robot.
    
    :param x: Coordonnée x du point
    :param y: Coordonnée y du point
    :param z: Coordonnée z du point
    :return: True si le point est dans la zone de travail, False sinon
    """
    if(theta2>0 and theta3<0):
        theta3 = -theta3
    elif(theta2<0) : 
        theta2 = -theta2
        
    #print("theta 1, 2,3",theta1,theta2,theta3)
    theta1 = np.radians(theta1)
    x, y, z = P_w
    max_x = 485.798*math.cos(theta1)
    #print(max_x)
    max_y = 485.798*math.sin(theta1)
    #print(max_y)
    max_z = 197.3 + 190.2*math.cos(np.radians(theta2))+247.6*math.cos(np.radians(theta3))
    #print(max_z)
    if x <= max_x and y <= max_y and z <= max_z:
        return True
    else:
        return True
    
def adapt_angle(angle):
    for i in range(len(angle)):
        if(angle[i]>180):
            angle[i] = -360 + angle[i]
        elif(angle[i]<-180):
            angle[i] = 360 - angle[i]
    
    return angle

def map_angle_to_motor_command(input_angle):
    # Plages d'entrée
    input_min = -140
    input_max = 140

    # Plages de sortie
    output_min = 0
    output_max = 180

    # Calcul de la commande du moteur
    output_command = (input_angle - input_min) * (output_max - output_min) / (input_max - input_min) + output_min

    # Limiter la sortie entre output_min et output_max
    output_command = max(output_min, min(output_max, output_command))

    return output_command


def max_angle_moteur():
    max_theta1 = 140
    min_theta1 = -140
    max_theta2 = 120
    min_theta2 = -120
    max_theta3 = -120
    min_theta3 = 120
    max_theta4 = 180
    min_theta4 = -180
    max_theta5 = -120
    min_theta5 = 120
    max_theta6 = -120
    min_theta6 = 120

# ------------------------------
# Partie principale du programme
# ------------------------------
def move_final_pose(P6, pitch, roll, yaw):
    #max x 485.798
    #max z 683.098
    # Données d'entrée
    

    # Conversion des angles d'orientation en radians pour la matrice de rotation
    R0_6 = compute_rotation_matrix(np.deg2rad(yaw), np.deg2rad(pitch), np.deg2rad(roll))
    
    # Paramètres géométriques (mm)
    d6 = 47.998

    print("Position de l'effecteur final :", P6)
    
    # Calcul de la position du poignet
    P_w = compute_wrist_position(R0_6, P6, d6)
    print(f"\nPosition du poignet sphérique : {P_w}\n")
    print(f"Position du poignet sphérique 2: {calculer_position_poignet(P6, np.radians(pitch), np.radians(roll), np.radians(yaw),d6)}\n")
    
    # Calcul des 3 premiers angles à partir de la position du poignet
    theta1, theta2, theta3 = compute_joint_angles(P_w)
    if in_limite_robot(P_w,theta1,theta2,theta3):
        print(f"Le point est dans la zone de travail du robot\n")
        print(f"Angles des 3 premiers joints : {[theta1, theta2, theta3]}\n") 
        # Vérification avec la cinématique directe du bras
        PS = compute_wrist_position_from_angle(theta1, theta2, theta3)
        #print(f"Position atteinte du poignet (cinématique directe du bras) : {PS}\n")
        # Calcul des 3 derniers angles (orientation du poignet)
        theta5, theta4, theta6 = compute_wrist_angles(R0_6, theta1, theta2, theta3,-pitch, roll, yaw)
        #test
        #theta4,theta5,theta6 = calcul_angles_4_5_6(theta1,P_w,P6)
        theta1,theta2,theta3,theta4,theta5,theta6 = adapt_angle([theta1,theta2,theta3,theta4,theta5,theta6])
        print(f"Angles des 3 derniers joints : {[theta4, theta5, theta6]}\n")
        # Conversion des angles pour les moteurs
        angle = [map_angle_to_motor_command(theta1),-(90 - map_angle_to_motor_command(theta2))+90,(90 - map_angle_to_motor_command(theta2))+90,-(90 - map_angle_to_motor_command(theta3))+90 ,(90- map_angle_to_motor_command(theta3))+90,map_angle_to_motor_command(theta4), map_angle_to_motor_command(theta5), map_angle_to_motor_command(theta6)]
        #print("Angle des moteurs : ", angle)
    else :
        print("Le point est en dehors de la zone de travaille du robot\n")










while True:
    command = input("Entrez la commande : 0 pour détacher les servos\n" 
                    +"1 pour attacher les servos\n"
                    +"2 pour enregistrer une position\n"
                    +"3 pour remettre a zéro les positions\n"
                    +"4 pour jouer la séquence enregistrée\n"
                    +"5 pour bouger par rapport à la position finale\n"
                    +"7 pour ouvrir la pince\n"
                    +"8 pour fermer la pince\n")

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
        x = float(input("Entrez le x :"))
        print("\n")
        y = float(input("Entrez le y :"))
        print("\n")
        z = float(input("Entrez le z :"))
        print("\n")
        pitch = float(input("Entrez le pitch :"))
        print("\n")
        roll = float(input("Entrez le roll :"))
        print("\n")
        yaw = float(input("Entrez le yaw :"))
        print("\n")
        angle = move_final_pose([x, y, z], pitch, roll, yaw)
        send_array(5, angle)

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






