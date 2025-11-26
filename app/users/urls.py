from django.urls import path
from .views import api_login, api_register


urlpatterns = [
    path("api/login/", api_login, name="api_login"),
    path("api/register/", api_register, name="api_register"),
]
