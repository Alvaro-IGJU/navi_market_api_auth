from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from companies.models import Chat, Message

class ChatMessagesView(APIView):
    """
    Devuelve los mensajes de un chat específico.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, chat_id):
        try:
            # Verificar si el chat existe y si el usuario es un participante
            chat = Chat.objects.prefetch_related("messages").get(id=chat_id, participants=request.user)

            # Obtener los mensajes del chat
            messages = chat.messages.order_by("timestamp").values(
                "id", "sender__username", "content", "timestamp"
            )

            return Response({"messages": list(messages)}, status=status.HTTP_200_OK)
        except Chat.DoesNotExist:
            return Response(
                {"error": "El chat no existe o no tienes acceso a él."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
