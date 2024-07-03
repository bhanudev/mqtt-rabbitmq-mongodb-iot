import paho.mqtt.client as mqtt
from pymongo import MongoClient
from datetime import datetime
from flask import Flask, request, jsonify

broker_host = '172.16.1.243'
broker_port = 1883
topic = 'status_updates'
mongo_uri = 'mongodb://localhost:27017/'
db_name = 'mqtt_db'
collection_name = 'status_data'

app = Flask(__name__)

client = MongoClient(mongo_uri)
db = client[db_name]
collection = db[collection_name]

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected to msg broker")
        client.subscribe(topic)
    else:
        print(f"connection failed with code {rc}")

def on_message(client, userdata, msg):
    try:
        status_message = eval(msg.payload.decode())
        status_message['timestamp'] = datetime.utcnow()
        collection.insert_one(status_message)
        print(f"stored message: {status_message}")
    except Exception as e:
        print(f"failed to store message: {e}")

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect(broker_host, broker_port, 60)
mqtt_client.loop_start()

@app.route('/status_count', methods=['get'])
def get_status_count():
    start_time = request.args.get('start')
    end_time = request.args.get('end')

    try:
        start_time = datetime.fromisoformat(start_time)
        end_time = datetime.fromisoformat(end_time)
    except ValueError:
        return jsonify({"error": "invalid date format"}), 400

    pipeline = [
        {"$match": {"timestamp": {"$gte": start_time, "$lt": end_time}}},
        {"$group": {"_id": "$status", "count": {"$sum": 1}}}
    ]

    result = list(collection.aggregate(pipeline))
    return jsonify(result)

if __name__ == "__main__":
    app.run(host= '172.16.1.243', port=5000)
