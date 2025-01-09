from django.urls import path
from companies.consumers import ChatConsumer

websocket_urlpatterns = [
    path("ws/companies/chats/<str:room_name>/", ChatConsumer.as_asgi()),
]
