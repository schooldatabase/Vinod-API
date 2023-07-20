from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from .consumers import ChatConsumer

application = ProtocolTypeRouter({
    'websocket': URLRouter([
        path('ws/chat/', ChatConsumer.as_asgi()),
    ]),
})