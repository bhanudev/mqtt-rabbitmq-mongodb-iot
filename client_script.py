import paho.mqtt.client as mqtt
import time
import random
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

broker_host = config.get('MQTT', 'broker_host')
broker_port = config.getint('MQTT', 'broker_port')
topic = config.get('MQTT', 'topic')

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected to broker")
    else:
        print(f"connection failed with code {rc}")

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect

mqtt_client.connect(broker_host, broker_port, 60)
mqtt_client.loop_start()

while True:
    status_message = {"status": random.randint(0, 6)}
    mqtt_client.publish(topic, str(status_message))
    print(f"sent message: {status_message}")
    time.sleep(1)

