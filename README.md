# MQTT Client-Server API with RabbitMQ and MongoDB
___
## Project Overview
This project involves the development of a client-server script in Python that handles MQTT messages via RabbitMQ. The client script emits MQTT messages every second with a field "status" containing a random value between 0 and 6. The server processes these messages, stores them in MongoDB, and provides an endpoint to accept start and end times to return the count of each status during the specified time range.

## Features

**MQTT Messaging Integration :** Utilizes RabbitMQ to manage and relay MQTT messages.
**Random Status Emission :** The client script sends a "status" value ranging from 0 to 6 every second.
**Message Processing and Storage :** The server processes incoming messages and stores them in MongoDB.
**Data Retrieval Endpoint :** An endpoint to retrieve the count of status messages within a specified time range using MongoDB’s aggregate pipeline.

## Project Structure

```plaintext
project_root/
│
├── config.ini                # Configuration file for setting broker, database, and server settings
├── client_script.py          # Client script for sending MQTT messages
├── server_script.py          # Server script for processing and storing messages, providing API endpoint
├── clientserverAPI.service   # systemd service file for running the scripts as a service
├── README.md                 # Project documentation
└── requirements.txt          # Python dependencies
```
# Getting Started
## Prequisites
- Python 3.7 or later.
- RabbitMQ with MQTT plugin enabled
- Mongo Db
- `systemd` for running the service

## Installing Dependencies
Create a virtual env and install python dependencies

> python3 -m venv myenv
> source myenv/bin/> activate
> pip install -r > requirements.txt

## Configurations
Copy the _**config.ini**_ file provided in the repository.


## Allow trafic on port 5000

> firewall-cmd --zone=public --add-port-5000/tcp --permanent
> firewall-cmd --zone=public --add-port-1883/tcp --permanent
> firewall-cmd --reload

## Enable MQTT Plugin
> rabbitmq-plugin enable rabbitmq_mqtt

## Configure RabbitMQ
Edit the configuration file
> vim /etc/rabbitmq/rabbitmq.conf

In the above configuration file copy the bellow settings

> Add the MQTT settings
> mqtt.default_user = guest
> mqtt.default_pass = guest
> mqtt.allow_anonymous = true
> mqtt.tcp_listeners = [1883]

# Running the project
##### Running the Scripts Manually
**Client_script**
>python client_script.py

**Server Script**
>python server_script.py

## Setting Up a Service
**place the clientserverAPI.service file in the systemd directory**

> cp clientserverAPI.service /etc/systemd/system/
> systemctl daemon-reload
> systemctl start clientserverAPI.service
> systemctl enable clientserverAPI.service

## Using the API

Access the API endpoint to get the status count

>Curl "http:server_ip//:5000/status_count?start=2024-07-02T00:00:00&end=2024-07-03T00:00:00"

Replace the start and end time parameter with your desired date-time format

# Troubleshooting
* connection Refused- Ensure Rabbitmq is running, and the MQTT plugin is enabled.

* MongoDB Connection issues- Verify MongoDB is up and running and the URI in config.ini is correct.

* Service Issues- Check logs using journalctl -u clientserverAPI.service for any errors or massages.
