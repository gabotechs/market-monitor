FROM python:3.8

WORKDIR /app

COPY ./requeriments.txt /app/requeriments.txt

RUN pip install -r requeriments.txt

COPY ./src/ /app/

ENTRYPOINT python main.py