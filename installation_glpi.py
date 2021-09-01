#!/usr/bin/python3
import apt
import subprocess
import mysql.connector
import wget
import tarfile
import shutil
import os

def install_maj(cache):

    cache.update()
    cache.open()
    cache.upgrade(True)
    cache.commit()

install_maj(apt.Cache())

liste_paquets = ['apache2', 'php', 'libapache2-mod-php', 'php-imap', 'php-ldap', 'php-curl',
                 'php-xmlrpc', 'php-gd', 'php-mysql', 'php-cas', 'mariadb-server', 'apcupsd',
               'php-apcu', 'php-intl', 'php-mbstring']

def install_paquets(liste):

    for pack in liste_paquets:
        print("installation de", pack)
        cache = apt.Cache()
        cache.update()
        pkg = cache[pack]
        if not pkg.is_installed:
            pkg.mark_install()

        cache.commit()

        cache.open()
        if cache[pack].is_installed:
            print(pack, "est maintenant installé")

install_paquets(liste_paquets)


def restart_services(service1,service2):

    subprocess.run(['systemctl', 'restart', service1])
    subprocess.run(['systemctl', 'status', service1])
    subprocess.run(['systemctl', 'restart', service2])
    subprocess.run(['systemctl', 'status', service2])

restart_services('apache2', 'mysql')


def create_database():

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

def install_glpi(url,path):

    filename = wget.download(url)

    tar = tarfile.open(filename, "r:gz")
    tar.extractall(path)
    tar.close()

install_glpi('https://github.com/glpi-project/glpi/releases/download/9.5.5/glpi-9.5.5.tgz',"/var/www/html/")


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


chown()

def config_glpi():

    subprocess.run(['php', '/var/www/html/glpi/bin/console', 'db:install', '-n', '-r', '-f', '-L', 'french', '-d', 'GLPIdb', '-u', 'glpiuser'])

config_glpi()

chown()

