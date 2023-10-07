import os
import requests
import json
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import argparse
from FileManagement import FileManagement
from MiningWorker import MiningWorker
#from writecsv import escrever_informacoes_em_csv  # Importe a função do módulo writecsv
from MinerWork import baixar_classes_java

# Função principal
def main():
    parser = argparse.ArgumentParser(description='Baixar classes Java de projetos no GitHub')
    parser.add_argument('--output', help='Caminho para o diretório de saída', default='java_classes')
    parser.add_argument('--csv', help='Nome do arquivo CSV de saída', default='informacoes.csv')  # Adicione um argumento para o nome do arquivo CSV
    args = parser.parse_args()
    
    output_dir = args.output
    os.makedirs(output_dir, exist_ok=True)

   # token = ler_configuracao()
    links = FileManagement.ler_links_projetos()
 
    informacoes_arquivos = ['Facade']  # Movido o dicionário para esta função
    termos_chave = informacoes_arquivos
    miningWorker = MiningWorker(links,"cloneRepository")
     
    for link in links:
        miningWorker.run()
        lista =  miningWorker.listarCommitGitLog()

        #apply filter in list commit of hash github
        for sha in lista:
            listaOnlyFileJava = miningWorker.getCommintHashPathFile(sha)
            for pathFile in listaOnlyFileJava:
                contentFile = miningWorker.getCommintInFile(sha, pathFile)
                print(contentFile.strip().decode('utf-8'))
                pathSave = 'output/' + sha + '/'+ pathFile
                FileManagement.saveFile(pathSave, contentFile.strip().decode('utf-8'))
    # Após o download, escreva as informações em um arquivo CSV
    #escrever_informacoes_em_csv(informacoes_arquivos, args.csv)  # Passe o nome do arquivo CSV como argumento


if __name__ == '__main__':
    main()