import os


def maj():
    os.system('sudo apt-get update && sudo apt-get upgrade')


maj()


def install_apache2():
    os.system('sudo apt-get install apache2 php libapache2-mod-php')


install_apache2()


def install_php():
    os.system('sudo apt-get install php-imap php-ldap php-curl php-xmlrpc php-gd php-mysql php-cas')


install_php()


def install_mariadb():
    os.system('sudo apt-get install mariadb-server')
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


def install_phpmyadmin():
    os.system('sudo apt-get install phpmyadmin')


install_phpmyadmin()


def install_glpi():
    os.system('cd /usr/src/')
    os.system('sudo wget https://github.com/glpi-project/glpi/releases/download/9.5.5/glpi-9.5.5.tgz')
    os.system('sudo tar -xvzf glpi-9.3.3.tgz -C /var/www/html')


install_glpi()


def droits_srv_lamp():
    os.system('sudo chown -R www-data /var/www/html/glpi/')


droits_srv_lamp()