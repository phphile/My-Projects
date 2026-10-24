
## Description du projet:
## Le projet a pour but de d'installer une configuration personnalisée automatiquement sur une VM vierge grâce au script shell. 
## Le fichier install_packages.sh installe et configure les paquets git, wget, curl et vim:
## pour git : installation et configuration  du nom et de l'addresse mail de l'utilisateur, de l'éditeur et de la branche principale du repo git 
## pour vim, curl et wget: installation et création du fichier config correspondant (.vimrc, .curlrc, .wgetrc) 
## Le fichier setup_shell.sh installe et configure zsh et oh-my-zsh:
## installation de zsh et le changer en shell par défaut 
## installation et configuration de oh-my-zsh et configuration du thème, des plugines, de l'auto-complétion des commandes et  des aliases 
## lancer le fichier .zshrc automatiquement pour activer les configuration
## Le fichier setup.sh regroupe install_packages.sh et setup_shell.sh

## Quelques fonctions non automatisées:
## les configurations pour wget, curl et vim ne sont pas incluses automatiquement 
## pas de génération de la clé ssh et de l'ajout à l'agent

## Instruction:
## Executer le fichier setup.sh pour lancer la configuration automatiquement 
## La liste des pacquets est incluse en haut du fichier install_packacges.sh. Il est possible de la modifier manuellement sans impacter l'installation automatique    
## La liste des plugins est aussi modifiable dans le fichier setup_shell.sh 

