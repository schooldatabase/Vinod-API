from django.urls import path, re_path
from . import consumers

websocket_urlpatterns = [
    #  re_path(r'ws/status/(?P<room_name>\w+)/$', consumers.StatusConsumer.as_asgi()),
    # re_path(r'ws/status/(?P<room_name>\w+)/$', consumers.StatusConsumer.as_asgi()),
    path('ws/chat/<room_name>/', consumers.UserProfileConsumer.as_asgi()),
    path('ws/chat/<room_name>/', consumers.ContactConsumer.as_asgi()),
    path('ws/chat/<room_name>/', consumers.MessageConsumer.as_asgi()),
    path('ws/status/<room_name>/', consumers.StatusConsumer.as_asgi()),
    path('ws/call/<room_name>/', consumers.CallConsumer.as_asgi()),
    path('ws/call/<room_name>/', consumers.NotificationSettingsConsumer.as_asgi()),
    
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