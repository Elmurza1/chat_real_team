from chat.routing import websocket_urlpatterns as chat_ws
from notifications.routing import websocket_urlpatterns as notifications_ws

websocket_urlpatterns = chat_ws + notifications_ws
