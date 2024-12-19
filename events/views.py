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
        print(request.data)
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
        try:
            # Obtener el evento
            event = Event.objects.get(pk=request.data["event"])
            print(request.data)
            # Validar si el evento alcanzó el número máximo de stands
            current_stand_count = Stand.objects.filter(event=event).count()
            if current_stand_count >= event.max_stands:
                return Response(
                    {"error": f"El evento '{event.name}' ya alcanzó el máximo de stands permitidos ({event.max_stands})."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Validar si ya existe un stand en la misma posición
            stands = Stand.objects.filter(event=event)
            for stand in stands:
                if int(stand.position) == int(request.data["position"]):
                    return Response(
                        {"error": "Ya existe un stand en esa posición."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            # Crear el stand
            serializer = StandSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Event.DoesNotExist:
            return Response(
                {"error": "El evento no existe."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": f"Error al crear el stand: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


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
    
