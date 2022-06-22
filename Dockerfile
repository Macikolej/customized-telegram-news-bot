FROM python:3.10-alpine

WORKDIR /app

RUN apk add --update --no-cache dumb-init mariadb-connector-c-dev gcc musl-dev

COPY ./crontab.txt ./
RUN crontab crontab.txt

COPY ./requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

ENTRYPOINT ["/usr/bin/dumb-init", "--"]

CMD ["python3", "entrypoint.py"]

