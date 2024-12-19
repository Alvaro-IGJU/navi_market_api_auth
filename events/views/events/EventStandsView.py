from rest_framework.views import APIView
from rest_framework.permissions import  AllowAny
from rest_framework import status
from events.models import Event, Stand
from rest_framework.response import Response
from events.serializers import StandSerializer


class EventStandsView(APIView):
    """
    Vista para listar los stands de un evento específico.
    """
    permission_classes = [AllowAny]  # Cambiar a IsAuthenticated si la autenticación es requerida.

    def get(self, request, event_id):
        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return Response({"error": "El evento no existe."}, status=status.HTTP_404_NOT_FOUND)

        # Filtrar los stands asociados al evento
        stands = Stand.objects.filter(event=event)
        serializer = StandSerializer(stands, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)