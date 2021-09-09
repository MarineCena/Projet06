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


def update(cache):
  try:
    cache.update()
    cache.open()
    cache.upgrade(True)
    cache.commit()
  except apt.cache.FetchFailedException:
    print("Failed, connexion error!")
  else:
    print("Update Sucessfull.")


def packs_install(liste_paquets):
  for pack in liste_paquets:
    print(pack, "is installing ...")
    try:
      cache = apt.Cache()
      cache.update()
      pkg = cache[pack]
      if not pkg.is_installed:
        pkg.mark_install()
        cache.commit()
    except apt.cache.FetchFailedException:
      print("Failed, connexion error!")
    else:
      cache.open()
      if cache[pack].is_installed:
        print(pack, "is now installed.")


def reboot_services(service):
  try:
    subprocess.run(['systemctl', 'restart', service])
  except FileNotFoundError:
    print("No such file or directory!")
  except subprocess.CalledProcessError as e:
    print(e.output)
  else:
    print(service, "service restarted.")


def create_database(conf, db):
  mydb = mysql.connector.connect(**conf)
  try:
    mycursor = mydb.cursor()
    mycursor.execute("CREATE DATABASE IF NOT EXISTS " + db)
  except mysql.connector.errors.ProgrammingError:
    print("Access denied!")
  else:
    print("Connected, database created.")


def create_user(conf,user):
  try:
    mydb = mysql.connector.connect(**conf)

    mycursor = mydb.cursor()
    mycursor.execute("DROP USER IF EXISTS " + user + "@localhost")
    mycursor.execute("CREATE USER " + user + "@localhost IDENTIFIED BY ''")
    mycursor.execute("grant all privileges on *.* to " + user + "@localhost")
  except mysql.connector.errors.ProgrammingError:
    print("Access denied!")
  except mysql.connector.errors.DatabaseError:
    print("User still exists!")
  else:
    print("User created.")


def glpi_download(url, path):
  try:
    filename = wget.download(url)
    tar = tarfile.open(filename, "r:gz")
    tar.extractall(path)
    tar.close()
  except tarfile.ExtractError:
    print("Extraction error!")
  except:
    print("Failed, connexion error!")
  else:
    print("GLPI is downloaded.")


def access_rights(path="/var/www/html/glpi", user='www-data', group=None, recursive=True):
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


def glpi_install():
  try:
    subprocess.run(['php', '/var/www/html/glpi/bin/console', 'db:install', '-n', '-r', '-f', '-L', 'french',
                    '-d', 'GLPIdb', '-u', 'glpiuser'])
  except subprocess.SubprocessError as e:
    print(e.output)
  else:
    print("GLPI is now installed.")


def del_file(file):
  try:
    os.remove(file)
  except PermissionError:
    print("access denied")
  except OSError:
    print("file doesn't exist!")
  else:
    print("File", (conf['FILEPATH']), "deleted!")

#Conf file reading
conf = read_conf('configuration.yml')
# Cache Update
update(apt.Cache())
# Packages' installation
packs_install(conf['LISTE'])
# Rebooting Apache2 and mysql services
reboot_services('apache2')
reboot_services('mysql')
# Database's creation
create_database(conf['CONFIG'], conf['DATABASE'])
# User's creation
create_user(conf['CONFIG'], conf['USER'])
# GLPI's installation
glpi_download(conf['URL'], conf['PATH'])
# Access righgts' assignements
access_rights()
# GLPI's configuration
glpi_install()
# Access righgts' assignements
access_rights()
# "install.php": file's deletion
del_file(conf['FILEPATH'])