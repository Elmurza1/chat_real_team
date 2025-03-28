from channels.db import database_sync_to_async
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from .models import Message

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    """Класс для обработки сообщений"""
    async def connect(self):
        """Подключение к сокету"""
        print("WebSocket подключен")
        self.user = self.scope['user']
        self.receiver_id = self.scope['url_route']['kwargs']['user_id']
        self.room_group_name = f"chat_{min(self.user.id, int(self.receiver_id))}_{max(self.user.id, int(self.receiver_id))}"

        if not self.user.is_authenticated:
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        """Отключение от сокета"""
        print(f"WebSocket отключен, причина: {close_code}")

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """Получение сообщений"""
        data = json.loads(text_data)
        message = data['message']
        sender = self.user
        # Обязательно ждем результата, так как get_receiver теперь асинхронная обёртка
        receiver = await self.get_receiver(self.receiver_id)

        # Обертка для создания сообщения в БД
        msg = await self.create_message(sender, receiver, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': msg.content,
                'sender': sender.username
            }
        )

    async def chat_message(self, event):
        """Отправка сообщений"""
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event["sender"],
        }))

    @database_sync_to_async
    def get_receiver(self, user_id):
        return User.objects.get(id=user_id)

    @database_sync_to_async
    def create_message(self, sender, receiver, content):
        return Message.objects.create(sender=sender, receiver=receiver, content=content)
