from channels.db import database_sync_to_async
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from .models import Message
from channels.layers import get_channel_layer
import redis

User = get_user_model()
redis_client = redis.Redis(host='localhost', port=6379, db=0)  # Подключение к Redis
channel_layer = get_channel_layer()


class ChatConsumer(AsyncWebsocketConsumer):
    """Класс для обработки сообщений"""

    async def connect(self):
        """Подключение к WebSocket"""
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

        # 🔥 Обнуляем счётчик непрочитанных сообщений в Redis
        unread_key = f"unread_{self.user.id}"
        redis_client.set(unread_key, 0)

        # 🔥 Отправляем обновлённый счётчик уведомлений пользователю
        await self.channel_layer.group_send(
            f"user_{self.user.id}",
            {
                "type": "new_message_notification",
                "sender": "",
                "message": "",
                "unread_count": 0,
            }
        )

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
        message_content = data['message']
        sender = self.user
        receiver = await self.get_receiver(self.receiver_id)

        # Сохраняем сообщение в БД
        message = await self.create_message(sender, receiver, message_content)

        # Отправляем сообщение в чат
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message.content,
                'sender': sender.username
            }
        )

        # ✅ Уведомление о новом сообщении
        await self.send_notification(receiver, sender.username, message_content)

    async def chat_message(self, event):
        """Отправка сообщений"""
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event["sender"],
        }))

    async def send_notification(self, receiver, sender_name, message):
        """Отправка WebSocket-уведомления + обновление счётчика непрочитанных сообщений"""
        unread_key = f"unread_{receiver.id}"
        redis_client.incr(unread_key)  # Увеличиваем счётчик непрочитанных

        await channel_layer.group_send(
            f"user_{receiver.id}",
            {
                "type": "new_message_notification",
                "sender": sender_name,
                "message": message,
                "unread_count": int(redis_client.get(unread_key)),
            }
        )

    @database_sync_to_async
    def get_receiver(self, user_id):
        return User.objects.get(id=user_id)

    @database_sync_to_async
    def create_message(self, sender, receiver, content):
        return Message.objects.create(sender=sender, receiver=receiver, content=content)
