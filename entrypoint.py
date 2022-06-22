import os
import subprocess

MODE = os.getenv("MODE")

if (MODE == "bot"):
	popen = subprocess.Popen('gunicorn app:app -b :8000', shell=True)
	popen.wait()
elif (MODE == "workers"):
	popen = subprocess.Popen("env >> /etc/environment", shell=True)
	popen.wait()
	popen = subprocess.Popen('crond -f -l 0', shell=True)
	popen.wait()
else:
	popen = subprocess.Popen('echo "internal error - wrong environmental variable"', shell=True)
