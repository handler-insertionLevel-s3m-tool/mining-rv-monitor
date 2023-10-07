import os
import requests
import json
from bs4 import BeautifulSoup
from urllib.parse import urlparse

global response

# Função para fazer uma solicitação HTTP com autenticação
def fazer_solicitacao(link, token):
    global response
    headers = {'Authorization': f'token {token}'}
    response = requests.get(link, headers=headers)
    return response


# Função para baixar um arquivo Java e verificar seu conteúdo antes de salvar
def baixar_arquivo_java(java_link, token, output_dir, termos_chave):
    java_file = fazer_solicitacao(java_link, token)
    if java_file.status_code == 200:
        file_name = os.path.basename(urlparse(java_link).path)
        content = java_file.text  # Lê o conteúdo do arquivo Java

        # Verifique se o conteúdo contém os termos-chave desejados
        if any(termo in content for termo in termos_chave):
            file_path = os.path.join(output_dir, file_name)  # Crie o caminho completo para o arquivo
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
                print(f'Arquivo Java baixado: {file_name}')
        else:
            print(f'O arquivo Java não contém os termos-chave: {file_name}')
    else:
        print(f'Erro ao baixar o arquivo Java: {java_link}')

# Função para baixar classes Java de um projeto GitHub e registrar informações
def baixar_classes_java(link, token, output_dir, informacoes_arquivos, termos_chave):
    response = fazer_solicitacao(link, token)
    listar_commits(token, link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links_java = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.java')]
        for java_link in links_java:
            baixar_arquivo_java(java_link, token, output_dir, termos_chave)
            # Registre informações sobre o arquivo baixado
            file_name = os.path.basename(urlparse(java_link).path)
            informacoes_arquivo = {
                'projeto': link,
                'classe': file_name,
                'path': os.path.join(output_dir, file_name)
            }
            informacoes_arquivos.append(informacoes_arquivo)  # Adicione ao dicionário
    else:
        print(f'Erro ao acessar o projeto GitHub: {link}')

def getUsuario():
    if response.status_code == 200:
        try:
            print(f"text da resposta: {response.text}")
            resultado = json.loads(response.text)
            if resultado.get("items"):
                # Recupere o nome do usuário/organização e nome do repositório do resultado da pesquisa
                usuario = resultado["items"][0]["owner"]["login"]
                print(f"Usuário/Organização: {usuario}")
            else:
                print(f"Nenhum usuário encontrado.")
        except ValueError:
            print(f"Erro na conversão do JSON: {ValueError}")
    else:
        print(f"Erro na solicitação à API do GitHub: {response.status_code}")     

def getRepositorio():
    if response.status_code == 200:
        resultado = response.json()
        if resultado.get("items"):
            # Recupere o nome do usuário/organização e nome do repositório do resultado da pesquisa
            repositorio = resultado["items"][0]["name"]
            print(f"Repositório: {repositorio}")
        else:
            print(f"Nenhum Repositório encontrado.")
    else:
        print(f"Erro na solicitação à API do GitHub: {response.status_code}") 

def listar_commits(token, link):  
    #response = fazer_solicitacao(link, token)
    
    usuario = getUsuario()
    repositorio = getRepositorio()

    api_url = f"https://api.github.com/repos/{usuario}/{repositorio}/commits"
    # Verifique se a solicitação foi bem-sucedida
    if response.status_code == 200:
        commits = response.json()
        if commits:
            print(f"Commits do repositório {usuario}/{repositorio}:")

            for commit in commits:
                hash_commit = commit["sha"]
                mensagem_commit = commit["commit"]["message"]
                print(f"- Hash: {hash_commit}, Mensagem: {mensagem_commit}")
        else:
            print(f"Nenhum commit encontrado no repositório {usuario}/{repositorio}.")
    else:
        print(f"Erro na solicitação à API do GitHub: {response.status_code}")
      