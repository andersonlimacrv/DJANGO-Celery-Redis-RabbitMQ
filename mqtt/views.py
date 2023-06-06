from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .mqtt_client import MQTTClient

mqtt_client = None  # Variável global para armazenar a instância do cliente MQTT


def broker_connection(request):
    global mqtt_client
    BROKER = "broker.emqx.io"
    PORT = 1883
    TOPIC = "python-mqtt/tls"
    USERNAME = ""
    PASSWORD = ""

    mqtt_client = MQTTClient(BROKER, PORT, TOPIC, USERNAME, PASSWORD)
    mqtt_client.connect()  # Conecta ao MQTT Broker

    return redirect("index_mqtt")


def broker_disconnection(request):
    global mqtt_client

    if mqtt_client is not None:
        mqtt_client.disconnect()
        mqtt_client = None

    return redirect("index_mqtt")


def index_mqtt(request):
    global mqtt_client

    is_connected = False
    message_list = []

    if request.method == "POST":
        # Verifica se o botão de conexão foi pressionado
        if "connect_btn" in request.POST:
            return redirect("broker_connection")
        if "disconnect_btn" in request.POST:
            return redirect("broker_disconnection")

        is_connected = mqtt_client is not None and mqtt_client.is_connected()

        if "payload" in request.POST:
            payload = request.POST.get("payload")
            mqtt_client.publish(payload)

    if mqtt_client is not None:
        message_list = mqtt_client.get_received_messages()

    context = {
        "mqtt_client": mqtt_client,
        "is_connected": is_connected,
        "message_list": message_list,
    }

    return render(request, "index_mqtt.html", context)


def mqtt_status(request):
    global mqtt_client

    if mqtt_client is None:
        return JsonResponse({"status": "Not connected"})

    # Lógica para obter o status atual do MQTT
    is_connected = mqtt_client.is_connected()

    status = "Connected" if is_connected else "Not connected"

    data = {"status": status}
    return JsonResponse(data)
