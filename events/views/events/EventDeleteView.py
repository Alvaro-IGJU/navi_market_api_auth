from rest_framework.views import APIView
from rest_framework.permissions import  IsAdminUser
from rest_framework import status
from events.models import Event
from rest_framework.response import Response

class EventDeleteView(APIView):
    """
    Vista para eliminar un evento (Solo administradores).
    """
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
            event.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Event.DoesNotExist:
            return Response({'error': 'Evento no encontrado'}, status=status.HTTP_404_NOT_FOUND)