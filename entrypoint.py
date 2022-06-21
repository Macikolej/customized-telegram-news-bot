import dotenv
import os
import subprocess

dotenv.load_dotenv()

MODE = os.getenv("MODE")

if (MODE == "bot"):
	popen = subprocess.Popen('gunicorn app:app -b :8000', shell = True)
elif (MODE == "workers"):
	popen = subprocess.Popen('python3 scraper.py', shell = True)
else:
	popen = subprocess.Popen('echo "internal error - wrong environmental variable"', shell = True)
