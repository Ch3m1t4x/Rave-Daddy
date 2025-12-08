from django.urls import path
from .views import chat_api, search_filter

urlpatterns = [
    path("send/", chat_api, name="chat_api"),
    path("filters/", search_filter, name="search_filter"),
]
