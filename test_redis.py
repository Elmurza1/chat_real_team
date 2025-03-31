import os
from channels.layers import get_channel_layer
import asyncio

# Указываем файл настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'a_core.settings')

async def test_redis_connection():
    layer = get_channel_layer()
    await layer.send("test_channel", {"type": "test.message", "text": "Hello, Redis!"})
    message = await layer.receive("test_channel")
    print("Сообщение из Redis:", message)

asyncio.run(test_redis_connection())
