g =9.81

masse_servo = 65

masse_obj = 350

Taille_bras_1 = 20
Taille_bras_2 = 25
Taille_bras_3 = 10

masse_bras_1 = 150
masse_bras_2 = 120
masse_bras_3 = 70

Position_servo_1 = 20
Position_servo_2 = 20
Position_servo_3 = 32.5
Position_servo_4 = 45
Position_servo_5 = 55

couple_servo = 17.5 


def conv_force (masse) : 
    masse = masse / 1000
    return masse * g

def affiche_force(force,num_servo) : 
    print(f"La force nécessaire pour le(s) servo(s) n°{num_servo} est de : {force} N.m soit {force * 0.1}Kg.cm")


#calcul du couple nécéssaire pour le servo du dernier axe
force_obj = conv_force(masse_obj) * (Position_servo_5 - Position_servo_4) + 10
force_tot_servo = conv_force(masse_servo) * (Position_servo_5 - Position_servo_4)
force_tot_bras = conv_force(masse_bras_3) * (Taille_bras_3 / 2)
couple_nc_3 = force_obj+force_tot_servo + force_tot_bras
affiche_force(couple_nc_3,6)
print("Le coef de sécurité est de :", ((17.5/(couple_nc_3*0.1))))



#calcul du couple necessaire pour les servos intermediaires
force_obj = conv_force(masse_obj) * (Position_servo_5 - Position_servo_1) + 10
force_tot_servo = conv_force(masse_servo) * (Position_servo_5 - Position_servo_2 + Position_servo_4 - Position_servo_2 + Position_servo_3 - Position_servo_2)
force_tot_bras = conv_force(masse_bras_2) * (Taille_bras_2 / 2 ) + conv_force(masse_bras_3) * (Taille_bras_3 / 2)
couple_nc_2 = force_obj+force_tot_servo + force_tot_bras
affiche_force(couple_nc_2,3.4)
print("Le coef de sécurité est de :", ((35/(couple_nc_2*0.1))))




#calcul de la force tot
force_obj = conv_force(masse_obj) * Position_servo_5 + 10
force_tot_servo = conv_force(masse_servo) * (Position_servo_1 + Position_servo_2 + Position_servo_3 + Position_servo_4 + Position_servo_5)
force_tot_bras = conv_force(masse_bras_1) * (Taille_bras_1/2) + conv_force(masse_bras_2) * (Taille_bras_2/2) + conv_force(masse_bras_3) * (Taille_bras_3 / 2)
couple_nc_1 = force_obj+force_tot_servo + force_tot_bras
affiche_force(couple_nc_1,1.2)
print("Le coef de sécurité est de :", ((35/(couple_nc_1*0.1))))










