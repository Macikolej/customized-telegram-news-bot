import os
import subprocess

MODE = os.getenv("MODE")

if (MODE == "bot"):
	popen = subprocess.Popen('gunicorn app:app -b :8000', shell=True)
	popen.wait()
elif (MODE == "workers"):
	popen = subprocess.Popen('python3 scraper.py', shell=True)
	popen.wait()
else:
	popen = subprocess.Popen('echo "internal error - wrong environmental variable"', shell=True)
