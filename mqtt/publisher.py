import json
import logging
import asyncio
from mqtt_client import MQTTClient


def publish_custom_payload():
    payload = {
        "msg1": "Hello, MQTT 1!",
        "msg2": "Hello, MQTT 2!",
        "msg3": "Hello, MQTT 3!",
    }
    mqtt_client.publish(payload)


async def start():
    logging.basicConfig(
        filename="mqtt.log",
        format="%(asctime)s - %(levelname)s: %(message)s",
        level=logging.DEBUG,
    )
    mqtt_client.connect()
    await asyncio.sleep(1)
    publish_custom_payload()  # Publica o payload personalizado
    while not FLAG_EXIT:
        await asyncio.sleep(1)


BROKER = "broker.emqx.io"
PORT = 1883
TOPIC = "python-mqtt/tls"
USERNAME = ""
PASSWORD = ""

FLAG_EXIT = False

if __name__ == "__main__":
    mqtt_client = MQTTClient(BROKER, PORT, TOPIC, USERNAME, PASSWORD)
    asyncio.run(start())
    mqtt_client.disconnect()
