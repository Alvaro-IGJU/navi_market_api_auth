from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from companies.models import Chat
from interactions.models import Interaction
from users.models import User

class CreateChatView(APIView):
    """
    Crea un chat entre dos usuarios si no existe y cambia el estado de la interacción a 'accepted'.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            participant_id = request.data.get("participant_id")
            company_id = request.data.get("company_id")

            if not participant_id or not company_id:
                return Response(
                    {"error": "El ID del participante y de la compañía son requeridos."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                participant = User.objects.get(id=participant_id)
            except User.DoesNotExist:
                return Response({"error": "El participante no existe."}, status=status.HTTP_404_NOT_FOUND)

            # Verificar si ya existe un chat entre estos usuarios
            existing_chat = Chat.objects.filter(
                participants=request.user
            ).filter(participants=participant).first()

            if existing_chat:
                return Response({"chat": {"id": existing_chat.id}}, status=status.HTTP_200_OK)

            # Crear un nuevo chat
            chat = Chat.objects.create()
            chat.participants.add(request.user, participant)
            chat.save()

            # Actualizar la interacción correspondiente
            interaction = Interaction.objects.filter(
                visit__user=participant,
                stand__company_id=company_id,
                interaction_type="schedule_meeting",
                status="pending"
            ).first()

            if interaction:
                interaction.status = "accepted"
                interaction.save()

            return Response({"chat": {"id": chat.id}}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
