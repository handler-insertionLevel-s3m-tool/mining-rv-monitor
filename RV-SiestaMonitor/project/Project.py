from project.ProcessRunner import ProcessRunner
import re

class Project:

    # Defina o padrão da expressão regular para verificar o padrão exato
    REMOTE_REPO_PATTERN = re.compile(r"((http|https)://)?.+\.com/.+/.+")
  
    def __init__(self, path, remote=True):
        self.path = path
        self.remote = Project.is_remote_repo(self.path)
        if self.remote:
            self.url = path
        else:
            self.url = None

    def getOwnerAndName(self):
        remoteUrl = self.getRemoteUrl()
        if remoteUrl is not None:
            splitPath = remoteUrl.split("/")
            projectName = splitPath[-1]
            projectOwner = splitPath[-2]
            return [projectOwner, projectName.replace(".git", "")]
        else:
            splitPath = self.path.split("/")
            projectName = splitPath[-1]
            return ["local", projectName.replace(".git", "")]

    def getRemoteUrl(self):
        if self.remote and Project.is_remote_repo(self.path):
            return self.path
        elif self.remote:
            process = ProcessRunner.runProcess(self.path, "git config --get remote.origin.url")
            return process.stdout.read().decode("utf-8").strip()
        else:
            return None   

    @staticmethod
    def is_remote_repo(path):
        # Use the match() function to check if the pattern matches the string
        match = Project.REMOTE_REPO_PATTERN.match(path)

        # If there is a match, the string meets the pattern
        return bool(match)     

    
          