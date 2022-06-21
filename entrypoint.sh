if [[ $MODE == "bot" ]]; then
	gunicorn app:app -b :8000
elif [[ $MODE == "workers" ]]; then
	python3 scraper.py
else
	echo "internal error - wrong environmental variable"
fi
