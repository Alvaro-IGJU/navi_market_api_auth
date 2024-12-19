from interactions.models import Visit
from events.models import Event
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status


class VisitRegisterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, event_id):
        user = request.user
        try:
            # Buscar el evento por su ID
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return Response({'error': 'Evento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        # Crear un nuevo registro de visita para este usuario y evento
        Visit.objects.create(
            user=user,
            event=event,
            time_spent_seconds=0,  # El tiempo será calculado en el cliente u otro flujo
            is_recurrent=False  # Siempre comienza como no recurrente
        )

        return Response({'message': 'Nueva visita registrada con éxito.'}, status=status.HTTP_201_CREATED)