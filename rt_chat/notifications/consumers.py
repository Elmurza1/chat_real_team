import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """ подключение к websocket """
        self.user = self.scop['user']

        if self.user.is_authenticated:
            self.room_group_name = f"notifications_{self.user.id}"

            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept

            unread_count = cache.get(f"unreal_messages_{self.user.id}", 0)
            await self.send(taxt_data=json.dumps({"unreal_count": unread_count}))


    async def disconnect(self):
        """ отключение websocket """

        if self.user.is_authenticated:
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name )

    async def send_notification(self, event):
        """ отправка самих уведомлений  """
        await self.send(text_data=json.dumps({"unreal_count": event["unreal_count"]}))
