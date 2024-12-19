# routing.py
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/CSDN_data/', consumers.CSDNDataConsumer.as_asgi()),
]
