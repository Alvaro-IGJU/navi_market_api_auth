from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from .models import Event, Stand
from rest_framework.response import Response
from .serializers import EventSerializer, StandSerializer


class EventListView(APIView):
    """
    Vista para listar todos los eventos (Acceso público).
    """
    permission_classes = [AllowAny]

    def get(self, request):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)


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


class EventCreateView(APIView):
    """
    Vista para crear un nuevo evento (Solo administradores).
    """
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

class StandListView(APIView):
    """
    Vista para listar todos los stands (Requiere autenticación).
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        stands = Stand.objects.all()
        serializer = StandSerializer(stands, many=True)
        return Response(serializer.data)


class StandCreateView(APIView):
    """
    Vista para crear un nuevo stand (Solo administradores).
    """
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = StandSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StandUpdateView(APIView):
    """
    Vista para actualizar un stand (Solo administradores).
    """
    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        try:
            stand = Stand.objects.get(pk=pk)
            serializer = StandSerializer(stand, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Stand.DoesNotExist:
            return Response({'error': 'Stand no encontrado'}, status=status.HTTP_404_NOT_FOUND)


class StandDeleteView(APIView):
    """
    Vista para eliminar un stand (Solo administradores).
    """
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        try:
            stand = Stand.objects.get(pk=pk)
            stand.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Stand.DoesNotExist:
            return Response({'error': 'Stand no encontrado'}, status=status.HTTP_404_NOT_FOUND)