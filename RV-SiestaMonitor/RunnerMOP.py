import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from FileManagement import ler_configuracao, ler_links_projetos

def execute_javamop(dir_path, class_name):
    javamop_command = f"javamop {dir_path} {class_name}.mop"
    os.system(javamop_command)

def execute_ajc(dir_path, class_name):
    ajc_command = f"ajc {dir_path} HashSetMonitorAspect.aj {class_name}/{class_name}.java -1.6 {class_name}/"
    os.system(ajc_command)

def navigate_to_class_directory(class_name):
    os.chdir(class_name)

def execute_java(class_name):
    java_command = f"java {class_name}"
    os.system(java_command)

# Substitua <dir> e <nomeDaClasse> pelos valores apropriados
dir_path = "<dir>"
class_name = "<nomeDaClasse>"

# Executar os passos em sequência
execute_javamop(dir_path, class_name)
execute_ajc(dir_path, class_name)
navigate_to_class_directory(class_name)
execute_java(class_name)
