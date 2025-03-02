import subprocess

command=['pyinstaller','--onefile','--noconsole','--icon=mine.ico','My first app.py']
subprocess.run(command)