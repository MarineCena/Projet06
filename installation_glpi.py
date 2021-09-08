#!/usr/bin/python3
import apt
import subprocess
import mysql.connector
import wget
import tarfile
import shutil
import os
import yaml


def install_maj(cache):

    try:
        cache.update()
        cache.open()
        cache.upgrade(True)
        cache.commit()
    except apt.cache.FetchFailedException:
        print("Fetching fails!")
    else:
        print("Update Sucessfull!")


def install_paquets(liste):
    with open('configuration.yml') as f:
        config = yaml.load(f)
        liste_paquets = (config['LISTE'])
        print(liste_paquets)

        for pack in liste_paquets:
            print("installation de", pack, "...")
            try:
                cache = apt.Cache()
                cache.update()
                pkg = cache[pack]
                if not pkg.is_installed:
                    pkg.mark_install()
                cache.commit()
            except apt.cache.FetchFailedException:
                print("Failed")
            else:
                cache.open()
                if cache[pack].is_installed:
                    print(pack, "est maintenant installé")

def restart_services(service):
    subprocess.run(['systemctl', 'restart', service])
    print("le service", (service), "a été redémarré")

def create_database():
    with open('configuration.yml') as f:
        config = yaml.load(f)
        conf = (config['CONFIG'])
    mydb = mysql.connector.connect(**conf)

    try:
        mycursor = mydb.cursor()
        mycursor.execute("CREATE DATABASE IF NOT EXISTS GLPIdatabase")

    except mysql.connector.errors.ProgrammingError:
        print("Access denied")

    else:
         print("connected, database created")

def create_user():
    try:
        with open('configuration.yml') as f:
            config = yaml.load(f)
            conf = (config['CONFIG'])
        mydb = mysql.connector.connect(**conf)

        mycursor=mydb.cursor()
        mycursor.execute("DROP USER IF EXISTS 'glpiuser'@'localhost'")
        mycursor.execute("CREATE USER 'glpiuser'@'localhost' IDENTIFIED BY ''")
        mycursor.execute("grant all privileges on *.* to 'glpiuser'@'localhost'")

    except mysql.connector.errors.ProgrammingError:
        print("Access denied")

    except mysql.connector.errors.DatabaseError:
        print("User exists")

    else:
         print("User created")


def install_glpi(url, path):

    try:
        filename = wget.download(url)
        tar = tarfile.open(filename, "r:gz")
        tar.extractall(path)
        tar.close()
    except tarfile.ExtractError:
        print("erreur extraction")
    except:
        print("Temporary failure in name resolution")
    else:
        print("Download sucessfull!")



def chown(path="/var/www/html/glpi", user='www-data', group=None, recursive=True):

    """
        Change user/group ownership of file

        :param path: path of file or directory
        :param str user: new owner username
        :param str group: new owner group name
        :param bool recursive: set files/dirs recursively

        """
    try:
        if not recursive or os.path.isfile(path):
            shutil.chown(path, user, group)
        else:
            for root, dirs, files in os.walk(path):
                shutil.chown(root, user, group)
                for item in dirs:
                    shutil.chown(os.path.join(root, item), user, group)
                for item in files:
                    shutil.chown(os.path.join(root, item), user, group)
    except OSError as e:
        raise UtilsException(e)

def config_glpi():

    subprocess.run(['php', '/var/www/html/glpi/bin/console', 'db:install', '-n', '-r', '-f', '-L', 'french', '-d', 'GLPIdb', '-u', 'glpiuser'])

def del_file(file):
    try:
        os.remove(file)

    except PermissionError:
        print("access denied")
    except OSError.filename:
        print("file doesn't exist!")
    else:
        print("File deleted!")


#Installer les mises à jour
install_maj(apt.Cache())
#Installer les différents paquets
install_paquets(liste_paquets)
#Redémarrer les services Apache2 et mysql
restart_services('apache2')
restart_services('mysql')
#Création de la base de données
create_database()
#Création de l'utilisateur
create_user()
#Installation GLPI avec la config yaml
with open('configuration.yml') as f:
    config = yaml.load(f)
    url = (config['URL'])
    path = (config['PATH'])
install_glpi(url, path)
#Attribution des droits d'accès
chown()
#Configuration de GLPI
config_glpi()
#Attribution des droits d'accès
chown()
#Suppression du fichier "install.php"
del_file("/var/www/html/glpi/install/install.php")





