#!/usr/bin/python3.6
import apt
import subprocess


def install_maj():

    cache = apt.Cache()
    cache.update()
    cache.open()
    cache.upgrade(True)
    cache.commit()

install_maj()

liste_paquets = ['apache2', 'php', 'libapache2-mod-php', 'php-imap', 'php-ldap', 'php-curl',
                 'php-xmlrpc', 'php-gd', 'php-mysql', 'php-cas', 'mariadb-server', 'apcupsd',
               'php-apcu']

def install_paquets():

    for pack in liste_paquets:
        print("installation de", pack)
        cache = apt.cache.Cache()
        cache.update()
        pkg = cache[pack]
        if not pkg.is_installed:
            pkg.mark_install()

        cache.commit()

        cache.open()
        if cache[pack].is_installed:
            print(pack, "est maintenant installé")

install_paquets()

def restart_services():
    subprocess.run(['/etc/init.d/apache2', 'restart'])
    subprocess.run(['/etc/init.d/mysql', 'restart'])

restart_services()


def create_database():
    import mysql.connector
    #from mysql.connector import errorcode

    mydb=mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="19022012",
        unix_socket="/var/run/mysqld/mysqld.sock"
    )
    mycursor=mydb.cursor()
    mycursor.execute("CREATE DATABASE IF NOT EXISTS GLPIdb")

create_database()


def create_user():
    import mysql.connector

    mydb=mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="19022012",
        unix_socket="/var/run/mysqld/mysqld.sock"
    )
    mycursor=mydb.cursor()
    mycursor.execute("DROP USER IF EXISTS 'glpiuser'@'localhost'")
    mycursor.execute("CREATE USER 'glpiuser'@'localhost' IDENTIFIED BY ''")
    mycursor.execute("grant all privileges on *.* to 'glpiuser'@'localhost'")

    mycursor.execute(" select User from mysql.user")

    for user in mycursor:
        if user == ('glpiuser',):
            print("l'utilisateur", (user), "a bien été crée")


create_user()

def install_glpi():
    import wget
    import tarfile

    url = 'https://github.com/glpi-project/glpi/releases/download/9.5.5/glpi-9.5.5.tgz'
    filename = wget.download(url)

    tar = tarfile.open(filename, "r:gz")
    tar.extractall("/var/www/html/")
    tar.close()

install_glpi()


def droits_srv_lamp():
    def chown(path="/var/www/html/glpi/", user='www-data', group=None, recursive=True):

        import shutil
        import os

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

    chown()

droits_srv_lamp()

def config_glpi():

    import subprocess
    #subprocess.run(['cd', '/var/www/html/glpi'])
    subprocess.run(['php', '/var/www/html/glpi/bin/console', 'db:install', '-L', 'french', '-d', 'GLPIdb', '-u', 'glpiuser'])

config_glpi()

