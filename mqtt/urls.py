from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_mqtt, name='index_mqtt'),
]