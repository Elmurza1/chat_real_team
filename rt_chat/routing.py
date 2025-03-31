from django.urls import re_path
from .consumers import ChatConsumer
from notifications.routing import websocket_urlpatterns as notifications_ws

# TODO: смотри ты делал уведамления и останавился к роутинг
#  если откроешь гпт чат то он там обяснит что да как так что доделай уведомления
websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<user_id>\d+)/$", ChatConsumer.as_asgi()),
]