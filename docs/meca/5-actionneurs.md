---
layout: home
nav_order: 5
title: Actionneurs et outils interchangeables
parent : Mécanique
---

Le robot a été conçu pour être compatible avec plusieurs outils interchangeables, qui peuvent être adaptés à différentes applications. Nous avons donc conçu deux types d’outils, le premier étant une pince motorisée qui est idéale pour le déplacement de pièce rigide. Le second outil est quant à lui une ventouse qui est donc plus adaptée à la manipulation d’objets délicats ou souples. Chaque outil est fixé au bout du sixième axe du robot a l’aide d’une fixation simple 
Pour la réalisation des outils, ceux-ci ont été modélisés avec l’utilisation des servomoteurs FT1025M qui sont de petits servomoteurs, ce qui rend les outils légers et précis. Pour la pince le moteur est donc monté à l’arrière de celle-ci dans le but de centrer les pinces afin d’éviter d’appliquer une correction à la trajectoire du robot.
Pour la ventouse, une boîte a été réalisée afin de comprimer l’air ou de créer une dépression. Cette boîte est donc située proche du boîtier d’alimentation, il permet de limiter le poids aux bouts du robot, ce qui permet donc de soulever des charges plus élevées
Afin de contrôler nos outils, ils sont contrôlés via l’Arduino, qui génère les signaux PWM nécessaires à leur contrôle
