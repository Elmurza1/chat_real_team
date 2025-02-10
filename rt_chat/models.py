from django.db import models
from django.contrib.auth.models import User

from PIL import Image
import os
# Create your models here.
class ChatGroup(models.Model):
    """ моделька для группы """
    group_name = models.CharField(max_length=100, unique=True, blank=True)
    group_chat = models.TextField(null=True, blank=True, )

    def __str__(self):
        return self.group_name



class GroupMessage(models.Model):
    """  моделька для сообщений в группе """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.message}"''

    class Meta:
        ordering = ['-created_at']

