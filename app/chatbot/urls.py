from django.urls import path
from .views import chat_api

urlpatterns = [
    path("send/", chat_api, name="chat_api"),
]
