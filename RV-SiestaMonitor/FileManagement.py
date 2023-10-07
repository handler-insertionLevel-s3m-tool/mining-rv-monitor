import csv
import os
import shutil
from project.Project import Project
from project.ProcessRunner import ProcessRunner

class FileManagement:

    @staticmethod
    def ler_configuracao():
        with open('config.csv', 'r') as configfile:
            configreader = csv.DictReader(configfile)
            for row in configreader:
                token = row['token']
        return token

    @staticmethod
    def ler_links_projetos():
        links = []
        with open('projetos.csv', 'r') as csvfile:
            csvreader = csv.DictReader(csvfile)
            for row in csvreader:
                link = row['link']
                project = Project(link)
                links.append(project)
        return links

    @staticmethod    
    def delete_directory(directory):
        if os.path.isfile(directory):
            os.remove(directory)
        elif os.path.isdir(directory):
            for item in os.listdir(directory):
                item_path = os.path.join(directory, item)
                if os.path.isfile(item_path):
                    os.remove(item_path)
                elif os.path.isdir(item_path):
                    FileManagement.delete_directory(item_path)
            os.rmdir(directory) 
    
    @staticmethod
    def delete_directory1(directory):
        shutil.rmtree(directory)
     
    @staticmethod 
    def saveFile(path, content):
        if not os.path.exists(path.replace('.java', '')):
          os.makedirs(path)
        caminho_arquivo = os.path.join(path, "File.java")

        try:
            with open(caminho_arquivo, "w") as arquivo:
                arquivo.write(content)
            print(f"Arquivo '{caminho_arquivo}' foi criado e salvo com sucesso.")
        except Exception as e:
            print(f"Ocorreu um erro ao criar ou salvar o arquivo: {str(e)}")
