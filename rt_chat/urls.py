from ckeditor_uploader.urls import urlpatterns
from django.urls import path
from .views import *


urlpatterns = [
    path('', home_view, name='home'),

    path('<int:user_id>/', chat_view, name='chat'),
]