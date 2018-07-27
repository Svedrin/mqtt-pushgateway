# mqtt-exporter

## Prometheus Exporter for metrics received via MQTT

This exporter works pretty much like the push gateway: You let it listen to
some interesting MQTT topics, it collects data into metrics and waits to
be scraped by Prometheus.

Caveat: Only float values are supported. Anything else will be ignored.

# Features

*   For each metric, a "metric_data_age" metric is exported that tells
    Prometheus when was the last time we received an update for this metric.

*   Allows metrics to expire if we don't get updates for a while.

*   Topics can be matched against a set of regular expressions to convert
    parts of their names into Prometheus keywords. Thus, a topic name such as

        sensor/garage/temperature

    when matched using regex

        sensor/(?P<sensor_name>\w+)/(?P<__metric__>\w+)

    would be exported to Prometheus as metric

        temperature{mqtt_topic="sensor/garage/temperature",sensor_name="garage"} 29.3

*   Topics can have individual expiry configurations.

*   Topics that were matched in a subscription pattern can be hidden from the
    result through a topic configuration.


# Installation

* `apt-get install python3-pytoml python3-paho-mqtt python3-flask`.
* Copy `config.example.toml` to `config.toml` and adapt it to your needs.
* Run mqtt-exporter.py. (See [mqtt-exporter.service](mqtt-exporter.service))
