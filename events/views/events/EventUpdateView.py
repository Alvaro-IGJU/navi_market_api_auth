from rest_framework.views import APIView
from rest_framework.permissions import  IsAdminUser
from rest_framework import status
from events.models import Event
from rest_framework.response import Response
from events.serializers import EventSerializer


class EventUpdateView(APIView):
    """
    Vista para actualizar un evento existente (Solo administradores).
    """
    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(event, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Event.DoesNotExist:
            return Response({'error': 'Evento no encontrado'}, status=status.HTTP_404_NOT_FOUND)
