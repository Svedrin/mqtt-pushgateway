#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# kate: space-indent on; indent-width 4; replace-tabs on;

import re
import pytoml
import logging
import socket
import time

import paho.mqtt.client as mqttClient

from collections import defaultdict
from datetime    import datetime

from flask import Flask, Response, redirect

app = Flask("mqtt_pushgateway")

with open("config.toml") as fd:
    config = pytoml.load(fd)


class Topic(object):
    def __init__(self):
        self.metric      = None
        self.keywords    = {}
        self.value       = None
        self.last_update = datetime.fromtimestamp(0)
        self.expire      = config["mqtt"].get("expire")
        self.ignore      = False

    def update(self, topic, value):
        # topic is e.g. sensors/somewhere/temperature
        # we want to apply our regexen, see if one matches
        # if one matches, use it to determine self.metric and self.keywords
        if self.metric is None:
            for cfg_topic in config["topic"]:
                if "match" in cfg_topic:
                    m = re.match(cfg_topic["match"], topic)
                    if m is not None:
                        self.keywords = m.groupdict()
                        self.expire = cfg_topic.get("expire")
                        self.ignore = cfg_topic.get("ignore", False)
                        if "__metric__" in self.keywords:
                            self.metric = self.keywords.pop("__metric__")
                        if "metric" in cfg_topic:
                            self.metric = cfg_topic["metric"]
                        break

            if self.metric is None:
                self.metric = topic.rsplit("/", 1)[1]

            if self.expire is None:
                self.expire = config["mqtt"].get("expire")

            self.keywords["mqtt_topic"] = topic

        self.value = value
        self.last_update = datetime.now()

    def __str__(self):
        data_age = (datetime.now() - self.last_update).total_seconds()

        if self.expire is not None and data_age > self.expire:
            # metric is expired, return data age only
            template =  '%(metric)s_data_age{%(kwds)s,mqtt_type="data_age"} %(age)f'
        else:
            template = ('%(metric)s{%(kwds)s,mqtt_type="value"} %(value)f\n'
                        '%(metric)s_data_age{%(kwds)s,mqtt_type="data_age"} %(age)f')

        return template % dict(
            metric = self.metric,
            kwds   = ','.join([ '%s="%s"' % item for item in self.keywords.items() ]),
            value  = self.value,
            age    = data_age
        )


metrics = defaultdict(lambda: Topic())


@app.route("/")
def http_index():
    return redirect("/metrics", code=302)

@app.route("/metrics")
def http_metrics():
    content = [str(metric)
        for metric in metrics.values()
        if not metric.ignore
    ]
    return Response('\n'.join(content + ['']), mimetype="text/plain")


def on_message(client, userdata, message):
    try:
        floatval = float(message.payload)
    except (TypeError, ValueError):
        logging.warning("Value is not a float: %s => %s", message.topic, message.payload)
    else:
        logging.info("Message received: %s => %s", message.topic, message.payload)
        metrics[message.topic].update(message.topic, floatval)


def main():
    client = mqttClient.Client(config["mqtt"]["client_id"] % dict(
        hostname=socket.gethostname()
    ))
    client.username_pw_set(config["mqtt"]["username"], config["mqtt"]["password"])
    client.on_message = on_message

    client.connect(config["mqtt"]["broker"], port=config["mqtt"]["port"])

    client.loop_start()

    for topic in config["mqtt"]["subscribe"]:
        client.subscribe(topic)

    app.debug = False

    try:
        app.run(host=config["exporter"]["listen"], port=config["exporter"]["port"])
    except KeyboardInterrupt:
        print("exiting")

    client.disconnect()
    client.loop_stop()


if __name__ == '__main__':
    main()
