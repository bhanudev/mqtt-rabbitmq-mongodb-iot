import time
import random
import paho.mqtt.client as mqtt

broker_host = '172.16.1.243'
broker_port = 1883

topic = 'status_updates'

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected successfully")
    else:
        print(f"connection failed with the result code {rc}")

def emit_status():
    client = mqtt.Client(protocol=mqtt.MQTTv311)
    client.on_connect = on_connect

    client.connect(broker_host, broker_port, 60)
    client.loop_start()

    try:
        while True:
            status = random.randint(0, 6)
            message = {"status": status}
            client.publish(topic, str(message))
            print(f"sent: {message}")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Disconnected")
        client.disconnect()

if __name__ == "__main__":
    emit_status()

