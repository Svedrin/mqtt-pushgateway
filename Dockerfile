FROM alpine:3.12

RUN apk add --no-cache python3 py3-pip

COPY . /app
WORKDIR /config

RUN pip3 install --no-cache-dir -r /app/requirements.txt

EXPOSE 9466
CMD [ "/usr/bin/python3", "/app/mqtt_pushgateway.py" ]
