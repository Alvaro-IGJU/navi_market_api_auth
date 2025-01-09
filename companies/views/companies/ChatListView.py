from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from companies.models import Chat

class ChatListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Obtener los chats donde participa el usuario
        chats = Chat.objects.filter(participants=user)

        # Preparar la respuesta
        response_data = []
        for chat in chats:
            last_message = chat.messages.order_by("-timestamp").first()  # Cambiado a `timestamp`
            response_data.append({
                "id": chat.id,
                "last_message": last_message.content if last_message else "No hay mensajes aún",
                "last_message_time": last_message.timestamp if last_message else None,
                "participants": [
                    {
                        "id": participant.id,
                        "username": participant.username,
                        "profile_picture": participant.profile_picture.url if participant.profile_picture else "/multimedia/images/default-avatar.jpg",
                    }
                    for participant in chat.participants.exclude(id=user.id)
                ],
            })

        return Response({"chats": response_data}, status=200)
