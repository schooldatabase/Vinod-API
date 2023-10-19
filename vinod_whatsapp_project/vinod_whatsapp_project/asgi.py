import os

from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
# from vinod_whatsapp1.routing import websocket_urlpatterns
import vinod_whatsapp1.routing 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vinod_whatsapp_project.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            vinod_whatsapp1.routing.websocket_urlpatterns
        ),
    ),
})


# application = ProtocolTypeRouter({
#     'http': get_asgi_application(),
#     'websocket': AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
# })














# import os
# from django.core.asgi import get_asgi_application


# # application = get_asgi_application()


# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter
# import vinod_whatsapp1.routing  # Import your app's routing configuration
# import django
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vinod_whatsapp_project.settings')

# # application = ProtocolTypeRouter({
# #     "http": get_asgi_application(),
# #     "websocket": URLRouter(vinod_whatsapp1.routing.websocket_urlpatterns),
# # })


# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             vinod_whatsapp1.routing.websocket_urlpatterns
#         ),
#     ),
# })


# import os

# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangopsql.settings')

# application = get_asgi_application()