from rest_framework.views import APIView
from users.permissions import  IsSuperUser
from rest_framework import status
from events.models import Stand
from rest_framework.response import Response
from events.serializers import StandSerializer

class StandUpdateView(APIView):
    """
    Vista para actualizar un stand (Solo administradores).
    """
    permission_classes = [IsSuperUser]

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