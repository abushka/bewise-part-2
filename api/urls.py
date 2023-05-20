from django.urls import path
from .views import create_user, add_audio

urlpatterns = [
    path('create-user/', create_user, name='create_user'),
    path('add-audio/', add_audio, name='add_audio'),
]