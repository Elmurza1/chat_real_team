from ckeditor_uploader.urls import urlpatterns
from django.urls import path
from .views import *


urlpatterns = [
    path('', chat_view, name='home')
]