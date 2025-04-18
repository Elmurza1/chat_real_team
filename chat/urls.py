from ckeditor_uploader.urls import urlpatterns
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_view, name='home'),

    path('<int:user_id>/', views.chat_view, name='chat'),
path('get-unread-counts/', views.get_unread_counts, name='get_unread_counts'),
    path('mark-as-read/<str:username>/', views.mark_as_read, name='mark_as_read'),
]