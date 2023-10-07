import subprocess
import os

class ProcessRunner:

    @staticmethod
    def runProcess(directory , command):   
        return ProcessRunner.processBuilder(directory , command)  
 
    @staticmethod 
    def processBuilder(directory , command): 
        process = subprocess.Popen(command, shell=True, cwd=directory, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

        return process

    @staticmethod
    def addCommand(subprocess, command):
        subprocess.Popen.args = command

    @staticmethod
    def startProcess():
        return subprocess.Popen.start()

    