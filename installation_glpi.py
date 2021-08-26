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


def create_bdd():
    import mysql.connector
    from mysql.connector import errorcode

    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="19022012",
            unix_socket="/var/run/mysqld/mysqld.sock",
            port="3306"
        )

        mycursor = mydb.cursor()

        mycursor.execute("CREATE DATABASE BDD")

        cnx = mysql.connector.connect(user='root',
                                      password='19022012',
                                      database='BDD')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cnx.close()

create_bdd()


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
    import shutil
    shutil.chown("/var/www/html/glpi/", "www-data")

droits_srv_lamp()

