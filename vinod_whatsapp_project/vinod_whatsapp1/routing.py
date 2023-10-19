from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/chat/', consumers.MessageConsumer),
]










# from django.urls import path
# from channels.routing import ProtocolTypeRouter, URLRouter
# from .consumers import ChatConsumer

# application = ProtocolTypeRouter({
#     # 'websocket': URLRouter([
#     #     path('ws/chat/', ChatConsumer.as_asgi()),
#     # ]),
# })


# from django.urls import re_path
# # from .consumers import ChatConsumer


# from . import consumers

# websocket_urlpatterns = [
#     # re_path(r'ws/some_path/$', consumers.ChatConsumer.as_asgi()),
#     # Add more URL patterns and consumers here as needed.
# ]