Feature: MQTT stuff.

  Scenario: Float values

    Given app is running
     when Topic sensor/bathroom/temperature receives message with payload "15.2"
     then Metric 'temperature{sensor_name="bathroom",mqtt_topic="sensor/bathroom/temperature"}' exists
      and its value is equal to 15.2
      and Metric 'mqtt_data_age{sensor_name="bathroom",mqtt_topic="sensor/bathroom/temperature",metric="temperature"}' exists
      and its value is less than 0.5

  Scenario: String values

    Given app is running
     when Topic sensor/bathroom/window receives message with payload "OPEN"
     then Metric 'window{sensor_name="bathroom",mqtt_topic="sensor/bathroom/window",window="OPEN"}' exists
      and its value is equal to 1.0
      and Metric 'mqtt_data_age{sensor_name="bathroom",mqtt_topic="sensor/bathroom/window",metric="window"}' exists
      and its value is less than 0.5
     when Topic sensor/bathroom/window receives message with payload "CLOSED"
     then Metric 'window{sensor_name="bathroom",mqtt_topic="sensor/bathroom/window",window="OPEN"}' exists
      and its value is equal to 0.0
      and Metric 'window{sensor_name="bathroom",mqtt_topic="sensor/bathroom/window",window="CLOSED"}' exists
      and its value is equal to 1.0
      and Metric 'mqtt_data_age{sensor_name="bathroom",mqtt_topic="sensor/bathroom/window",metric="window"}' exists
      and its value is less than 0.5
