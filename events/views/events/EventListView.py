from rest_framework.views import APIView
from events.models import Event
from rest_framework.permissions import  AllowAny
from events.serializers import EventSerializer
from rest_framework.response import Response


class EventListView(APIView):
    """
    Vista para listar todos los eventos (Acceso público).
    """
    permission_classes = [AllowAny]

    def get(self, request):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)