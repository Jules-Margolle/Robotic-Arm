g =9.81

masse_servo = 65

masse_obj = 100

Taille_bras_1 = 19.2
Taille_bras_2 = 24.76
Taille_bras_3 = 6

masse_bras_1 = 121
masse_bras_2 = 106
masse_bras_3 = 29
masse_patin = 20
masse_bague = 14
masse_roulement = 36
masse_outil = 20

Position_servo_1 = Taille_bras_1
Position_servo_2 = Taille_bras_1
Position_servo_3 = Taille_bras_1 + Taille_bras_2/2
Position_servo_4 = Taille_bras_1 + Taille_bras_2/2
Position_servo_5 = Taille_bras_1 + Taille_bras_2 + Taille_bras_3

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
force_acces =  conv_force(masse_outil) * ((6.6385/2)+52.1)
couple_nc_3 = force_obj+force_tot_servo + force_tot_bras + force_acces
affiche_force(couple_nc_3,6)
print("Le coef de sécurité est de :", ((couple_servo/(couple_nc_3*0.1))))



#calcul du couple necessaire pour les servos intermediaires
force_obj = conv_force(masse_obj) * (Position_servo_5 - Position_servo_1) + 10
force_tot_servo = conv_force(masse_servo) * (Position_servo_5 - Position_servo_2 + Position_servo_4 - Position_servo_2 + Position_servo_3 - Position_servo_2)
force_tot_bras = conv_force(masse_bras_2) * (Taille_bras_2 / 2 ) + conv_force(masse_bras_3) * (Taille_bras_3 / 2)
#force pour les accesoires
force_accs = conv_force(masse_bague) * ((2.92/2) + 29.7465) + conv_force(masse_roulement) * ((3.3850/2)+27.6521) + conv_force(masse_outil) * ((6.6385/2)+52.1)
couple_nc_2 = force_obj+force_tot_servo + force_tot_bras + force_accs
affiche_force(couple_nc_2,3.4)
print("Le coef de sécurité est de :", ((couple_servo * 2/(couple_nc_2*0.1))))




#calcul de la force tot
force_obj = conv_force(masse_obj) * Position_servo_5 + 10
force_tot_servo = conv_force(masse_servo) * (Position_servo_1 + Position_servo_2 + Position_servo_3 + Position_servo_4 + Position_servo_5)
force_tot_bras = conv_force(masse_bras_1) * (Taille_bras_1/2) + conv_force(masse_bras_2) * (Taille_bras_2/2) + conv_force(masse_bras_3) * (Taille_bras_3 / 2)
couple_nc_1 = force_obj+force_tot_servo + force_tot_bras
affiche_force(couple_nc_1,1.2)
print("Le coef de sécurité est de :", ((couple_servo *2/(couple_nc_1*0.1))))


#nouveau calcul total
#calcul force necessaire pour l'objet
force_necessaire = conv_force(masse_obj) * Position_servo_5 + 10
#calcul force nécessaire pour les bras
force_necessaire = force_necessaire + conv_force(masse_bras_1) * Taille_bras_1/2 + conv_force(masse_bras_2) * Taille_bras_2/2 + conv_force(masse_bras_3) * Taille_bras_3/2
#calcul force nécessaire pour les servos
force_necessaire = force_necessaire + conv_force(masse_servo) * (Position_servo_1 + Position_servo_2 + Position_servo_3 + Position_servo_4 + Position_servo_5)
#calcul force nécéssaire pour les accesoire en plus des bras
force_necessaire = force_necessaire + conv_force(masse_patin) * ((7.45/2)+12.9) + conv_force(masse_bague) * ((2.92/2) + 29.7465) + conv_force(masse_roulement) * ((3.3850/2)+27.6521) + conv_force(masse_outil) * ((6.6385/2)+52.1)

affiche_force(force_necessaire,1.5)
print("Le coef de sécurité est de :", ((couple_servo *2/(force_necessaire*0.1))) )









