import numpy as np
import multiprocessing
from tqdm import tqdm
import csv
from datetime import datetime
import math
import itertools
import numpy as np
import math

def get_rpy_from_matrix(R):
  """
  Extrait les angles de Roll, Pitch et Yaw d'une matrice de rotation 3x3.
  """
  roll = math.atan2(R[2, 1], R[2, 2])  # atan2(R32, R33)
  pitch = math.asin(-R[2, 0])         # asin(-R31)
  yaw = math.atan2(R[1, 0], R[0, 0])   # atan2(R21, R11)
  return roll, pitch, yaw


def matrice_DH_modifiee(parametres):
    matrices_DH = []
    for alpha, d, theta,a  in parametres:
        #print(alpha, d, theta, a)
        matrice = np.array([
            [math.cos(theta), -math.sin(theta), 0, d],
            [math.cos(alpha)*math.sin(theta), math.cos(alpha) * math.cos(theta), -math.sin(alpha), -a * math.sin(alpha)],
            [math.sin(alpha)*math.sin(theta), math.sin(alpha)*math.cos(alpha), math.cos(alpha), a* math.cos(alpha)],
            [0, 0, 0, 1]
        ])
        matrices_DH.append(matrice)
    return matrices_DH

# Créer un verrou global (en dehors de la fonction)
lock = multiprocessing.Lock()

def write_csv(bdd):
    with lock:
        filename = "BDD_robot.csv"
        with open(filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            for row in bdd:  # Itérer sur les lignes de bdd
                writer.writerow(row) # Écrire chaque ligne individuellement


#calcul de la matrice finale de dh 
def calcul_dh(t1, t2, t3, t4, t5, t6):
    parametres = [
        [0, 0, np.radians(t1), 197.3],  # Exemple: t1 = 0
        [math.pi/2, 0, np.radians(t2)+math.pi/2, 0],  # Exemple: t2 = 0
        [0, 190.2, np.radians(t3)-math.pi/2, 0],  # Exemple: t3 = 0
        [-math.pi/2, 0, np.radians(t4), 247.6],  # Exemple: t4 = 0
        [math.pi/2, 0, np.radians(t5), 0],  # Exemple: t5 = 0
        [-math.pi/2, 0, np.radians(t6), 47.998]  # Exemple: t6 = 0
    ]
    matrices_DH = matrice_DH_modifiee(parametres)
    T_global = np.eye(4)  # Matrice identité 4x4
    for matrice in matrices_DH:
        T_global = np.dot(T_global, matrice)
    position = T_global[:3, 3]  # [x, y, z]
    rotation_matrix = T_global[:3, :3]  # Matrice de rotation
    roll, pitch, yaw = get_rpy_from_matrix(rotation_matrix)
    roll = math.degrees(roll)
    pitch = math.degrees(pitch)
    yaw = math.degrees(yaw)
    position = np.append(position, [roll, pitch, yaw])
    
   # print("Position:", position)
    
    # print("Roll:", roll)
    # print("Pitch:", pitch)
    # print("Yaw:", yaw)
    # print("\n\n")
    
    return position



def calcul_dh_and_write(args):
    """Calcule DH et écrit dans le CSV.  Fonction pour le pool."""
    t1, t2, t3, t4, t5, t6 = args
    pos = calcul_dh(t1, t2, t3, t4, t5, t6)
    args = np.append(args, pos)
    return [str(x) for x in args]

pos = calcul_dh(0,0,0,0,0,0)
print(pos)

#def main():
#     """Fonction principale pour la parallélisation."""
    
#     bdd = []
    
#     # Générer toutes les combinaisons d'angles
#     step = 9
#     MAX_ANGLE = 46
#     MIN_ANGLE = -45

#     angle_combinations = itertools.product(
#         range(MIN_ANGLE, MAX_ANGLE, step),
#         range(MIN_ANGLE, MAX_ANGLE, step),
#         range(MIN_ANGLE, MAX_ANGLE, step),
#         range(MIN_ANGLE, MAX_ANGLE, step),
#         range(MIN_ANGLE, MAX_ANGLE, step),
#         range(MIN_ANGLE, MAX_ANGLE, step)
#     )

#    # Convertir l'itérateur en liste pour connaître sa taille
#     angle_combinations_list = list(angle_combinations)
#     total_combinations = len(angle_combinations_list)

#     num_processes = multiprocessing.cpu_count()
#     print(f"\nNombre de processus: {num_processes}")
#     print("Début de la génération de la base de données...")

#     bdd = []
#     with multiprocessing.Pool(processes=num_processes) as pool:
#         # Utiliser tqdm pour afficher la progression
#         with tqdm(total=total_combinations, desc="Combinaisons d'angles", unit="combinaison") as pbar:
#             for result in pool.imap_unordered(calcul_dh_and_write, angle_combinations_list):
#                 bdd.append(result)
#                 pbar.update(1)
        
    

#     print("Fin de la génération de la base de données.")
#     print("Ecriture dans le fichier CSV...")
#     write_csv(bdd)
#     print("Ecriture terminée.\n")

# if __name__ == "__main__":
#     main()

    
