Pour mettre le code dans la raspi :
  - Mettre le code sur une clé usb
  - brancher la clé sur la raspi et aloler voir dans /media si elle est reconnue
  - Si elle est reconnue on va juste dans le répertoire sinon il faut taper la commande lsblk qui montre tous les périphériques connectés, normalement la clé s'appellera "sda1", à chaque fois qu'on débranche et rebranche la clé elle change de nom "sdb1", "sdc1"...
  - il y a dossier /mnt/usb pour monter manuellement les clé usb, il faut taper "sudo mount /dev/(nom de la clé) /mnt/usb
  - Plus qu'a se déplacer dans le dossier /mnt/usb et executer le programme
