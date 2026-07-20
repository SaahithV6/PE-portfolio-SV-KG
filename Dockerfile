FROM python:3.9-slim-buster

WORKDIR /myportfolio

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

RUN chmod +x docker-entrypoint.sh

CMD ["./docker-entrypoint.sh"]

EXPOSE 5000
