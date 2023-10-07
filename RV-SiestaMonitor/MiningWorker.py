import os
from FileManagement import FileManagement
from project.ProcessRunner import ProcessRunner
from project.Project import Project

class MiningWorker:
    #projetos = []
    diretory = ""
    def __init__(self, project, base_dir):
        self.projects = project
        self.base_dir = base_dir
        
    def run(self):

        while len(self.projects) > 0:
            try:
                # Acesse o primeiro elemento da lista
                project = self.projects[0]
        
                # Remova o primeiro elemento da lista
                self.projects.pop(0)
                if project.remote:
                    self.diretory =  self.base_dir + "/" + project.getOwnerAndName()[1]
                    target = self.base_dir 
                    self.cloneRepository(project, self.base_dir )

            except Exception as e:
                # Capturando a exceção e lidando com ela
                print(f"Ocorreu uma exceção: {e}")        
                    
    def cloneRepository(self, project, target):
        print(f'Cloning repository {project.getOwnerAndName()[1]} into {target}')    

        # caso exista o diretório, apague-o 
        if not os.path.exists(target):
            os.makedirs(target)
        else:
            FileManagement.delete_directory1(target)     

        url = project.url
        
        if FileManagement.ler_configuracao() != None:
            token = FileManagement.ler_configuracao()
          #  url = f'https://{token}@github.com/{project.getOwnerAndName()[0]}/{project.getOwnerAndName()[1]}.git' 
            url = f'https://{token}@github.com/{project.getOwnerAndName()[0]}/{project.getOwnerAndName()[1]}.git' 
        command = f'git clone {url}'    

        process = ProcessRunner.runProcess(target, command)
        process.wait()
        print(f'Clone finished repository {project.getOwnerAndName()[1]} into {target}') 

    def listarCommitGitLog(self):
        print(f'Listing hash commit ')    

        commits = []
        try:
            target = self.diretory
            command = 'git --no-pager log --pretty=format:%H'
            process = ProcessRunner.runProcess(directory=self.diretory,command=command)

            # Aguarde o subprocesso terminar
            process.wait()

            # Leia e imprima a saída padrão
            for linha in process.stdout:
                commits.append(linha.strip().decode('utf-8'))
                print(linha.strip().decode('utf-8'))


                # Verifique se houve algum erro no stderr
            erros = process.stderr.read()
            if erros:
                print("Erros:", erros)
            return commits
        except process.CalledProcessError as e:
            print("Erro ao executar o comando:", e)   

    def getCommintHashPathFile(self,sha):
        print(f'Listing files: {sha}')
        listaOnlyFileJava = []
        command = f'git ls-tree -r {sha} --name-only'
        process = ProcessRunner.runProcess(directory=self.diretory,command=command)
        listPath = process.stdout
        for path in listPath:
            if path.strip().decode('utf-8').endswith(".java"):
                listaOnlyFileJava.append(path.strip().decode('utf-8'))
                print("ONly java:" + path.strip().decode('utf-8'))
            print(path)
        print(listPath)
        return listaOnlyFileJava
    
    def getCommintInFile(self,sha, pathFile):
        command = f'git show {sha}:{pathFile}'
        process = ProcessRunner.runProcess(directory=self.diretory,command=command)
        outputFile = process.stdout
        contentFile = outputFile.read()
        print(contentFile)
        return contentFile 
          