#!/usr/bin/python3
import apt
import subprocess
import mysql.connector
import wget
import tarfile
import shutil
import os
import yaml

def read_conf(file):
  with open(file) as f:
      return yaml.load(f)


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


def install_paquets(liste_paquets):
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
    try:
        subprocess.run(['systemctl', 'restart', service])
    except FileNotFoundError:
        print("No such file or directory")
    except subprocess.CalledProcessError as e:
        print(e.output)
    else:
        print((service), "restarted")

def create_database(conf):
    mydb = mysql.connector.connect(**conf)
    try:
        mycursor = mydb.cursor()
        mycursor.execute("CREATE DATABASE IF NOT EXISTS GLPIdb")
    except mysql.connector.errors.ProgrammingError:
        print("Access denied")
    else:
         print("connected, database created")

def create_user(conf):
    try:
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
    try:
        subprocess.run(['php', '/var/www/html/glpi/bin/console', 'db:install', '-n', '-r', '-f', '-L', 'french', '-d', 'GLPIdb', '-u', 'glpiuser'])
    except subprocess.SubprocessError as e:
        print(e.output)

def del_file(file):
    try:
        os.remove(file)
    except PermissionError:
        print("access denied")
    except OSError:
        print("file doesn't exist!")
    else:
        print("File", (conf['FILEPATH']), "deleted!")

conf = read_conf('configuration.yml')
#Installer les mises à jour
install_maj(apt.Cache())
#Installer les différents paquets
install_paquets(conf['LISTE'])
#Redémarrer les services Apache2 et mysql
restart_services('apache2')
restart_services('mysql')
#Création de la base de données
create_database(conf['CONFIG'])
#Création de l'utilisateur
create_user(conf['CONFIG'])
#Installation de GLPI
install_glpi(conf['URL'], conf['PATH'])
#Attribution des droits d'accès
chown()
#Configuration de GLPI
config_glpi()
#Attribution des droits d'accès
chown()
#Suppression du fichier "install.php"
del_file(conf['FILEPATH'])





