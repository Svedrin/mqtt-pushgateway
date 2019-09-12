FROM python:3.7-slim-buster

RUN apt-get update && apt-get -y install python3-pytoml python3-paho-mqtt python3-flask

COPY . /app
WORKDIR /config

EXPOSE 9466
CMD [ "/app/mqtt-pushgateway.py" ]
