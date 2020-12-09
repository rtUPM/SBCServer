#!/usr/bin/python3
import os
import time
import sys
import paho.mqtt.client as mqtt
import json
import subprocess

SERVER = '127.0.0.1'
ACCESS_TOKEN = ''

sensor_data = {'temperature': 0, 'humidity': 0, 'heater': 0, 'humidifier': 0}

next_reading = time.time()

client = mqtt.Client()

# Set access token
client.username_pw_set(ACCESS_TOKEN)

# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(SERVER, 1883, 60)

data = subprocess.run(['/home/pi/SBCServer/scripts/getSensorData.sh'], stdout=subprocess.PIPE).stdout.decode().rstrip()
temperature, humidity, heater, humidifier = data.split()
print("Temperature: %s, Humidity: %s Heater: %s Humidifier: %s" % (temperature, humidity, heater, humidifier))
sensor_data['temperature'] = temperature
sensor_data['humidity'] = humidity
sensor_data['humidifier'] = humidifier
sensor_data['heater'] = heater

client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)

client.disconnect()

