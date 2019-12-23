# encoding: utf-8

from time import sleep
from behave import given, when, then

import mqtt_pushgateway

def get_metrics():
    prom_data = mqtt_pushgateway.http_metrics().data.decode("UTF-8")

    def floatify(line):
        key, val = line.split()
        return key, float(val)

    return dict([
        floatify(line)
        for line in prom_data.split("\n")
        if line
    ])

@when('Topic {topic} receives message with payload "{payload}"')
def step(context, topic, payload):
    context.dirty = True
    context.publish(topic, payload.encode("UTF-8"))

@when('Topic {topic} receives message of')
def step(context, topic):
    context.dirty = True
    context.publish(topic, context.text.encode("UTF-8"))

@then("Metric '{metric}' exists")
def step(context, metric):
    # Refresh context.metrics if necessary
    if context.dirty or not context.metrics:
        sleep(0.1)
        context.metrics = get_metrics()

    if metric not in context.metrics:
        print("####\nMetric does not exist:\n   %s\nThese metrics do exist:\n%s\n####\n" % (
            metric, "\n".join([ " * %s" % m for m in context.metrics])
        ))
        assert metric in context.metrics, "metric does not exist, see stdout for details"

    context.metric_value = context.metrics[metric]

@then("its value is equal to {value:f}")
def step(context, value):
    assert context.metric_value == value, "Value %f is not == %f" % (context.metric_value, value)

@then("its value is less than {value:f}")
def step(context, value):
    assert context.metric_value < value, "Value %f is not < %f" % (context.metric_value, value)

@then("its value is more than {value:f}")
def step(context, value):
    assert context.metric_value > value, "Value %f is not > %f" % (context.metric_value, value)
