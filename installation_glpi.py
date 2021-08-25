import apt
import subprocess


def install_maj():
# First of all, open the cache
    cache = apt.Cache()
# Now, lets update the package list
    cache.update()
# We need to re-open the cache because it needs to read the package list
    cache.open()
# Now we can do the same as 'apt-get upgrade' does
    cache.upgrade()
# or we can play 'apt-get dist-upgrade'
    cache.upgrade(True)
# Q: Why does nothing happen?
# A: You forgot to call commit()!
    cache.commit()

#install_maj()

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

#install_paquets()

def restart_services():
    subprocess.run(['/etc/init.d/apache2', 'restart'])
    subprocess.run(['/etc/init.d/mysql', 'restart'])

#restart_services()


def create_bdd():
    import mysql.connector

    mydb = mysql.connector.connect(
        host="localhost",
        user="yourusername",
        password="yourpassword"
    )

    mycursor = mydb.cursor()

    mycursor.execute("CREATE DATABASE mydatabase")


create_bdd()


def install_glpi():
    subprocess.run(["cd /usr/src/", "sudo wget https://github.com/glpi-project/glpi/releases/download/9.5.5/glpi-9.5.5.tgz",
                   "sudo tar -xvzf glpi-9.5.5.tgz -C /var/www/html"])

#install_glpi()


def droits_srv_lamp():
    subprocess.run(["sudo chown -R www-data /var/www/html/glpi/"])


#droits_srv_lamp()