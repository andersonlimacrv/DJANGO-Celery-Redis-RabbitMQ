import paho.mqtt.client as mqtt
import logging
import random
import time
import json
import asyncio


class MQTTClient:
    def __init__(self, broker, port, topic, username, password):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.username = username
        self.password = password
        self.client_id = f"CLIENT_ID_{random.randint(0, 1000)}"
        self.client = mqtt.Client(self.client_id)
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message
        self.received_messages = []

    def connect(self):
        self.client.will_set(
            self.topic,
            payload=f"Client {self.client_id} Disconnected",
            qos=1,
            retain=False,
        )
        self.client.username_pw_set(self.username, self.password)
        self.client.connect(self.broker, self.port, keepalive=3)
        self.client.loop_start()

    def disconnect(self):
        self.client.disconnect()
        self.client.loop_stop()
        logging.info("Disconnected from MQTT Broker!")

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0 and client.is_connected():
            logging.info("Connected to MQTT Broker!")
            client.subscribe(self.topic)
            self.client.publish(
                self.topic,
                payload=f"Client {self.client_id} Connected",
                qos=1,
                retain=False,
            )
        else:
            logging.error(f"Failed to connect, return code {rc}")

    def on_disconnect(self, client, userdata, rc):
        logging.info("Disconnected with result code: %s", rc)
        if rc != 0:
            logging.info("Publishing Last Will message...")
            self.publish(f"{self.client_id} Disconnected")
        reconnect_count, reconnect_delay = 0, 1
        while reconnect_count < 12:
            logging.info("Reconnecting in %d seconds...", reconnect_delay)
            time.sleep(reconnect_delay)

            try:
                self.client.reconnect()
                logging.info("Reconnected successfully!")
                return
            except Exception as err:
                logging.error("%s. Reconnect failed. Retrying...", err)

            reconnect_delay *= 2
            reconnect_delay = min(reconnect_delay, 60)
            reconnect_count += 1
        logging.info("Reconnect failed after %s attempts. Exiting...", reconnect_count)
        global FLAG_EXIT
        FLAG_EXIT = True

    def on_message(self, client, userdata, msg):
        logging.info(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        self.received_messages.append(
            msg.payload.decode()
        )  # Adiciona a mensagem recebida à lista

    def publish(self, payload):
        if not self.client.is_connected():
            logging.error("publish: MQTT client is not connected!")
            return
        msg = json.dumps(payload)
        result = self.client.publish(self.topic, msg)
        status = result.mid
        if status == mqtt.MQTT_ERR_SUCCESS:
            logging.info(f"Send `{msg}` to topic `{self.topic}`")
        else:
            logging.error(f"Failed to send message to topic {self.topic}")

    def is_connected(self):
        return self.client.is_connected()

    def get_received_messages(self):
        return self.received_messages

    async def start(self):
        logging.basicConfig(
            filename="mqtt.log",
            format="%(asctime)s - %(levelname)s: %(message)s",
            level=logging.DEBUG,
        )
        self.connect()
        while not FLAG_EXIT:
            await asyncio.sleep(1)

        self.disconnect()


BROKER = "broker.emqx.io"
PORT = 1883
TOPIC = "python-mqtt/tls"
USERNAME = ""
PASSWORD = ""

FLAG_EXIT = False

if __name__ == "__main__":
    mqtt_client = MQTTClient(BROKER, PORT, TOPIC, USERNAME, PASSWORD)
    asyncio.run(mqtt_client.start())
    mqtt_client.disconnect()
