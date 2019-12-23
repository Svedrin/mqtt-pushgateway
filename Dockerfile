FROM alpine:latest

RUN apk add --no-cache python3

COPY . /app
WORKDIR /config

RUN pip3 install --no-cache-dir -r /app/requirements.txt

EXPOSE 9466
CMD [ "/usr/bin/python3", "/app/mqtt_pushgateway.py" ]
