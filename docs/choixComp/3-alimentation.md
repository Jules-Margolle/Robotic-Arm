---
layout: home
nav_order: 3
title: Alimentation
parent : Choix des composants
---

Les servomoteurs consomment au maximum 2,4 A par moteur (d'après nos tests réalisés). Pour être sûr de pouvoir les alimenter correctement, nous avons décidé de considérer 3 A par moteur :  

 

3 x 8 = 24 A  

 

Les servos moteurs ont une plage d’alimentation entre 4,8 et 8,4 V.  

Plus la tension d’alimentation est élevée, plus leur couple est important.  

  

Avec une alimentation de 8 V : 8 * 24 = 192 W.  

 

Les tensions d'alimentation standard sont de 5 V ou de 12 V, sans intermédiaire.   

Sur les alimentations à découpage, une vis permet de régler la tension de sortie d’environ 15 %. Même en considérant la plage de réglage de 15 %, nous ne pourrons pas obtenir la tension d’alimentation idéale.   

 

- 12*0,85 = 10,2 V  

- 5*1,15 = 5,75 V  

   

Nous pouvons utiliser des hacheurs Buck pour réduire la tension de 12 V à 8 V. Leur coût est très faible par rapport aux bénéfices en termes de puissance. De plus, les alimentations en 12 V sont moins chères que celles en 5 V à puissance équivalente.   

Pour cette plage de tension et d'ampérage, le LM2596 est un module adapté. Son rendement est annoncé à 94 %. En considérant un rendement de 90 % :   

- 192*1,10 = 211.2 W  

   

   

LRS150F-5 -> 30€ alimentation 5V 20A  

12V 30A ->26€ -> Amazon  

LM2596 -> convertisseur BUCK -> 0.99€/10 (aliexpress) ou 14€/10 (Amazon)  

   

L’alimentation de la carte Raspberry Pi se fera à part, pour éviter les variations de tension dues au servomoteur (celui-ci y étant très sensible). Elle nous revient à 11.69€ l’unité et donc 23.38€ pour nous car nous en prenons deux.