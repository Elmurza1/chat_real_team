import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    """ класс для обработки сообщений """
    async def connect(self):
        """ подключение к сокету """
        self.room_group_name = 'chat_room'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()


    async def disconnect(self, close_code):
        """ отключение от сокета """
        await self.channel_layer.group_discard(
              self.room_group_name,
              self.channel_name
          )

    async def receive(self, text_data):
        """  получение сообщений """
        data = json.loads(text_data)
        message = data['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        """ отправка сообщений """
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))
