import os
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

# Импортируем маршруты WebSocket
from chat.routing import websocket_urlpatterns as chat_ws
from notifications.routing import websocket_urlpatterns as notifications_ws

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "a_core.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(chat_ws + notifications_ws)  # Объединяем маршруты чата и уведомлений
    ),
})
