---
layout: home
nav_order: 2
title: Le(s) microcontrôleur(s)
parent : Choix des composants
---

Les besoins du Microcontrôleur :   
<ul>
<li>Ressource en calcul importants</li>   

<li>A terme projet de vision pour le contrôle du robot.</li>   

<li>Calcul de matrice pour le contrôle des mouvements</li>  

<li>Conversion des matrices en signal pour les moteurs</li>  

<li>Branche GPIO pour le contrôle des moteurs ou accessoires</li>   

<li>Entrée analogique pour le feedback des moteurs</li>  

<li>Connectique WI-FI pour le contrôle à distance depuis un ordinateur</li>  

<li>Idéalement la possibilité de programmer avec plusieurs langages pour s’adapter au besoin au choix logiciel.</li>   
</ul>
   

L’ESP32 et les cartes Arduino ne seront pas adaptées par manque de ressources en calcul. Quant à la Raspberry Pi, elle ne possède pas d’entrée analogique, mais il est possible d’ajouter un composant sur les GPIO pour percevoir les retours des servos et convertir les signaux analogiques en numériques.   

Pour cela, il est possible d’utiliser un composant comme le ADS1115 qui communique via le protocole I2C.  

Pour limiter les coûts, nous pouvons également utiliser une carte Arduino (que nous n’avons pas besoin d’acheter) possédant des entrées analogiques et qui pourra communiquer avec la Raspberry via différents protocoles possibles.   

   

Enfin, pour faciliter le contrôle des servos et limiter les besoins en calculs, il est possible d’utiliser une carte comme la PCA9685 qui s’occupera de générer les signaux PWM envoyés au servo moteur. Celle-ci est adaptée à la Raspberry Pi et se fixe directement dessus environ 20 €.  