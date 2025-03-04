---
layout: home
nav_order: 5
title: Récapitulatif et matériaux
parent : Choix des composants
---

| Composant | Prix |
|:-:|:-:|
| Convertisseur BUCK x 10 | 14€ | 
| Raspberry Pi | 20€ | 
| Ventilateur |  14.26€ | 
| Bouton AU | 11.98€ | 
| Alimentation 5V 20A | 26€ | 
| Moteur x 8 | 117.2€ | 
| Actionneur |  27€ |
| Palonnier moteur x 10|  24€ | 
| Moteur actionneur x 2|  27€ | 
| Caméra  | 29.99€ | 
|Total||

## Taille du Bras :  

La taille du robot dépend principalement de l’utilisation qui en sera faites. Dans notre cas le robot doit uniquement attraper une pièce en mouvement sur un convoyeurs de 1,20m. Nous n’avons pas de contrainte particulière sur l’endroit auquel la pièce doit être attrapé ni de la position de l’outil (pitch, roll, yaw) au moment où la pièces et prise. Etant donné que le robot peut atteindre une multitude de position dans son champ d’action, si l’on place le robot au centre du convoyeur, il pourra atteindre la pièce sur une zones environ égale à deux fois sa taille totale. Dans notre cas uniquement un champ d’action d’une dizaine de centimètre serait suffisant pour prendre la pièce. Or étant donné que le projet est voué à être repris et amélioré. Nous avons décidé d’avoir une taille bien supérieure, lui permettant d’éventuelles autres utilisations ou contrainte d’utilisation. Sur cette base nous avons choisi un objectif de taille de 60 cm car cela permettait d’atteindre la majeure partie du convoyeur sans engendrer des forces nécessitant des moteurs extrêmement puissants. 

## Choix des matériaux :   

Pour le choix des matériaux utilisés lors de l'impression 3D, plusieurs options s’offrent à nous, Pour les différentes pièces principales du robot, nous avons eu le choix entre le PLA et le PETG. Le PETG est plus résistant mais il est aussi et surtout plus cassant. Nous avons donc choisi le PLA car celui-ci est recyclable et économique, mais aussi car celui-ci a un comportement plus « élastique » ce qui lui permet de se déformer et non de casser lors des chocs.
Le PLA nous permet donc de créer des pièces de grandes tailles avec des caractéristiques mécaniques adaptés à notre usage mais aussi d’obtenir des pièces suffisamment résistantes et très légères.
   


## Roulement :  

Les roulements actuellement utilisés sur le robot sont entièrement imprimés en 3D et sont par conséquent soumis à une usure rapide. Pour pallier ce problème, les roulements vont être imprimés en iglidur. (Filament autolubrifié de chez igus). Malgré ce matériau l’usure sera tout de même plus prononcée qu'avec des roulements en métal qui sont beaucoup plus lourd. Étant donné que le robot est un prototype, les roulements fait en impression 3D seront gardés dans un premier temps pour conserver la légèreté nécessaire au robot pour pouvoir fonctionner avec les moteurs choisis.   

Néanmoins il est possible d'utiliser des roulements en métal mais il faudra pour cela changer les moteurs de l’axe N°2. Ceux-ci peuvent être remplacer par des moteurs brushless identique aux nôtres mais beaucoup plus puissant et moins sensible à l'usure (également beaucoup plus chère). À titre d'indication les roulements en métal pèsent environ 65g à eux seul tandis que notre système pèse 20 g pour l'ensemble roulement/fixations.   

