FROM python:3.10-alpine

WORKDIR /app

RUN apk add --update --no-cache dumb-init

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

ENTRYPOINT ["/usr/bin/dumb-init", "--"]

CMD ["gunicorn", "app:app"]

