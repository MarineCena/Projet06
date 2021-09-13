
![Python 3](https://img.shields.io/badge/python-3.6%2B-green)
![Linux](https://img.shields.io/badge/Compatible-Linux-white)

# INSTALLATION ET CONFIGURATION AUTOMATIQUE DE GLPI


> INTRODUCTION 

Dans le cadre du projet 6 « Participez à la vie de la communauté OpenSource » de la formation « Administrateur Infrastructure & Cloud » d’OpenClassrooms, je dois développer un programme permettant d’automatiser une ou plusieurs tâches au choix. 

Il s’agit donc d’un programme en python qui permet d’installer et de configurer le logiciel GLPI afin d‘obtenir directement, lors de la connexion à l’URL « adresseIP/glpi », la page de connexion de GLPI (identifiant glpi ; mdp : glpi).



> PRE-REQUIS 

Avant de lancer le programme sur votre machine il est impératif de télécharger les paquets suivants :
* « Python3-apt »
* Le module python « mysql-connector-python »
* Le module python « wget »
*    « php-simplexml » peut être nécessaire sous Debian


> EXECUTION DU SCRIPT

Le script doit être lancé depuis le terminal via la commande au choix :
* Python3 Installation_glpi.py
* ./Installation_glpi.py

![exe1](https://zupimages.net/up/21/35/zh7x.png)
![exe2](https://zupimages.net/up/21/35/8mxy.png)





> CONNEXION AU SERVEUR

Une fois que le script a été exécuté rendez-vous sur votre navigateur préféré. Si vous l'avez lancé avec le fichier de configuration original, il vous suffit d'entrer votre adresse IP suivie de « /GLPI ». Vous obtiendrez alors la page de connexion de GLPI comme ci-dessous
L’identifiant et le mot de passe par défaut sont respectivement : glpi ; glpi.

![co]( https://zupimages.net/up/21/35/s3i1.png) 


