from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from interactions.models import Interaction
from django.db.models import Q

class RejectScheduleMeetingView(APIView):
    """
    Marca una solicitud de schedule meeting como rechazada.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user_id = request.data.get("user_id")
            company_id = request.data.get("company_id")

            if not user_id or not company_id:
                return Response(
                    {"error": "El ID del usuario y el ID de la compañía son requeridos."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Buscar la interacción pendiente del tipo "schedule_meeting"
            interaction = Interaction.objects.filter(
                interaction_type="schedule_meeting",
                visit__user_id=user_id,
                stand__company_id=company_id,
                status="pending"
            ).first()

            if not interaction:
                return Response(
                    {"error": "No se encontró una interacción pendiente para este usuario."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Cambiar el estado de la interacción a "rejected"
            interaction.status = "rejected"
            interaction.save()

            return Response(
                {"message": "Solicitud rechazada con éxito."},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
