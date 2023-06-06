from django.urls import path
from . import views

urlpatterns = [
    path("", views.index_mqtt, name="index_mqtt"),
    path("mqtt_status/", views.mqtt_status, name="mqtt_status"),
    path("broker_connection", views.broker_connection, name="broker_connection"),
    path(
        "broker_disconnection", views.broker_disconnection, name="broker_disconnection"
    ),
]
