import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from chat.models import Message
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """ подключение к websocket """
        self.user = self.scope['user']

        if self.user.is_authenticated:
            self.room_group_name = f"notifications_{self.user.id}"

            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        """ отключение websocket """
        if self.user.is_authenticated:
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        """ получение сообщений """
        data = json.loads(text_data)
        action = data['action']

        if action == 'get_unread_count':
            unread_count = int(redis_client.get(f"unread_count_{self.user.id}") or 0)
            await self.send(text_data=json.dumps({'unread_count': unread_count}))

    async def new_message_notification(self, event):
        """ отправка уведомления о новом сообщении """
        await self.send(text_data=json.dumps({
            'type': 'new_message_notification',
            'message': event['message'],
            'sender': event['sender'],
            'unread_count': event['unread_count'],
        }))
