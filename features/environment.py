import threading

from time import time, sleep

import paho.mqtt.client as mqtt

import mqtt_pushgateway

def before_all(context):
    client = mqtt.Client(client_id="IT")
    client.connect("broker", 1883)

    def publish(topic, payload):
        client.publish(topic, payload)

    context.publish = publish

    context.mqtt_pushgateway = threading.Thread(target=mqtt_pushgateway.main)
    context.mqtt_pushgateway.daemon = True
    context.mqtt_pushgateway.start()
    sleep(0.1)

def before_scenario(context, scenario):
    context.dirty = True
    context.metrics = {}
