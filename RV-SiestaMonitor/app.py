from subprocess import Popen, PIPE
from pathlib import Path
from project.ProcessRunner import ProcessRunner
import os

def main():
  #diretory='C:\\UFPE\\Siesta\\RV-SiestaMonitor\\cloneRepository\\mobilePhone\\mobilePhone'
  diretory='cloneRepository/mobilePhone/mobilePhone/mobilePhone'

  command = 'git --no-pager log --pretty=format:%H'
  process = ProcessRunner.runProcess(diretory,command)

            # Aguarde o subprocesso terminar
  stdout, stderr = process.communicate()
 # print(process.stdout.readlines().count())

  retorno = process.returncode
  print(retorno)
  print(stdout)
  print(process.stdout)
  print(process.stderr)
  print(process.stdin)
  print(process.args)
  print(process.pid)
  print(process.returncode)
  print(process.poll())
  print(process.terminate())
  print(process.kill())

if __name__ == "__main__":
    main()