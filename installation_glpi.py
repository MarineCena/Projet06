import apt
import os

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
liste_paquets = ['apache2', 'php', 'libapache2-mod-php', 'php-imap', 'php-ldap', 'php-curl', 'php-xmlrpc',
                 'php-gd ', 'php-mysql', 'php-cas', 'mariadb-server', 'apcupsd php-apcu', 'phpmyadmin']


def install_pkg():
    cache = apt.cache.Cache()
    cache.update()
    pkg = cache[pkg]

    for pkg in liste_paquets:

        print(pkg)
        if not pkg.is_installed:
            pkg.mark_install()

            cache.commit()

            cache.open()
            if cache[pkg].is_installed:
                print(pkg, "est maintenant installé")

            pkg += 1

"""
install_apache2()

def install_php():
    cache = apt.cache.Cache()
    cache.update()
    pkg = cache[pack2]

    if not pkg.is_installed:
        pkg.mark_install()

    cache.commit()

    cache.open()
    if cache[pack2].is_installed:
        print(pack2, "est maintenant installé")
    #os.system('sudo apt-get install php-imap php-ldap php-curl php-xmlrpc php-gd php-mysql php-cas')

install_php()



def install_mariadb():
    cache = apt.cache.Cache()
    cache.update()
    pkg = cache[pack5]

    if not pkg.is_installed:
        pkg.mark_install()

    cache.commit()

    cache.open()
    if cache[pack5].is_installed:
        print(pack5, "est maintenant installé")

    os.system('sudo mysql_secure_installation')


install_mariadb()


def install_modules_comp():
    os.system('sudo apt-get install apcupsd php-apcu')


install_modules_comp()


def restart_services():
    os.system('/etc/init.d/apache2 restart')
    os.system('/etc/init.d/mysql restart')


restart_services()


def create_bdd():
    os.system('sudo mysql -u root -p')


create_bdd()


#def install_phpmyadmin():
    #os.system('sudo apt-get install phpmyadmin')


#install_phpmyadmin()


def install_glpi():
    os.system('cd /usr/src/')
    os.system('sudo wget https://github.com/glpi-project/glpi/releases/download/9.5.5/glpi-9.5.5.tgz')
    os.system('sudo tar -xvzf glpi-9.5.5.tgz -C /var/www/html')


install_glpi()


def droits_srv_lamp():
    os.system('sudo chown -R www-data /var/www/html/glpi/')


droits_srv_lamp()
"""