from django.shortcuts import render, redirect
from django.http import HttpResponse
def index_mqtt(request):
    return render(request, 'index_mqtt.html')