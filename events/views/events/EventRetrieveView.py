from rest_framework.views import APIView
from rest_framework.permissions import  AllowAny
from rest_framework import status
from events.models import Event
from events.serializers import EventSerializer
from rest_framework.response import Response


class EventRetrieveView(APIView):
    """
    Vista para obtener los detalles de un evento específico (Acceso público).
    """
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(event)
            return Response(serializer.data)
        except Event.DoesNotExist:
            return Response({'error': 'Evento no encontrado'}, status=status.HTTP_404_NOT_FOUND)

