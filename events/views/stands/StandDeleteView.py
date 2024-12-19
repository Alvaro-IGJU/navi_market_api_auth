from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from events.models import Stand
from rest_framework.response import Response

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
        

    
