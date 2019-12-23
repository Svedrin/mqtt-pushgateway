# Prometheus Exporter for metrics received via MQTT

This exporter provides a push gateway for MQTT: You let it listen to
some interesting MQTT topics, it collects data into metrics and waits to
be scraped by Prometheus.

Messages that can be parsed as JSON will log a unique metric per key:value pair
using a 'virtual' topic of `topic/key`.

Caveat: Only float values are supported. Anything else will be ignored.

# Features

*   Topics can be matched against a set of regular expressions to convert
    parts of their names into Prometheus keywords. Thus, a topic name such as

        sensor/garage/temperature

    when matched using regex

        sensor/(?P<sensor_name>\w+)/(?P<__metric__>\w+)

    would be exported to Prometheus as metric

        temperature{mqtt_topic="sensor/garage/temperature",sensor_name="garage"} 29.3

*   Each metric is accompanied by an `mqtt_data_age` metric, that tells us
    when the last update occurred:

        mqtt_data_age{mqtt_topic="sensor/garage/temperature",sensor_name="garage",metric="temperature"} 7

    By setting a threshold on this value, you can detect and alert on sensors
    being broken somehow and not sending updates anymore.

*   Allows metrics to expire if we don't get updates for a while. When a metric
    expires, its value won't be exported anymore, but data_age will continue
    to be exported. Thus, you can expire a metric after 2 minutes, but only
    after 5 minutes send an alert.

    Each Topic can have an individual expiry configuration.

*   Topics that were matched in a subscription pattern can be hidden from the
    result through a topic configuration.

*   JSON messages record each key:value pair as a unique metric, eg: the following payload sent on topic `zigbee2mqtt/sensor/lounge/xiaomi/WSDCGQ01LM`:

        {"temperature":29.02,"linkquality":34,"humidity":55.58,"battery":100,"voltage":3005}

    would expose the following metrics:

        temperature{mqtt_topic="zigbee2mqtt/sensor/lounge/xiaomi/WSDCGQ01LM/temperature"} 29.020000
        linkquality{mqtt_topic="zigbee2mqtt/sensor/lounge/xiaomi/WSDCGQ01LM/linkquality"} 34.000000
        humidity{mqtt_topic="zigbee2mqtt/sensor/lounge/xiaomi/WSDCGQ01LM/humidity"} 55.580000
        battery{mqtt_topic="zigbee2mqtt/sensor/lounge/xiaomi/WSDCGQ01LM/battery"} 100.000000
        voltage{mqtt_topic="zigbee2mqtt/sensor/lounge/xiaomi/WSDCGQ01LM/voltage"} 3005.000000

# Installation

* `apt-get install python3-pytoml python3-paho-mqtt python3-flask`.
* Copy `config.example.toml` to `config.toml` and adapt it to your needs.
* Run `mqtt_pushgateway.py`. (See [mqtt-pushgateway.service](mqtt-pushgateway.service))


# Docker

You can also use Docker:

* `docker build -t mqtt-exporter:latest .`
* `docker run -p 9466:9466 -v config.toml:/config/config.toml mqtt-exporter:latest`
