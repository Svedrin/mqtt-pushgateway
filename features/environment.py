from time import time

import paho.mqtt.client as mqtt

def before_all(context):
    client = mqtt.Client(client_id="IT")
    client.connect("broker", 1883)

    def publish(topic, payload):
        client.publish(topic, payload)

    context.publish = publish
