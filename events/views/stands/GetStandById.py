from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from events.models import Stand
from rest_framework.response import Response
from rest_framework import status
from events.serializers import StandSerializer


class GetStandByIdView(APIView):
    """
    Vista para obtener un stand por su ID (Requiere autenticación).
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, stand_id):
        try:
            stand = Stand.objects.get(id=stand_id)
            serializer = StandSerializer(stand)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Stand.DoesNotExist:
            return Response(
                {"error": "Stand no encontrado."}, status=status.HTTP_404_NOT_FOUND
            )
