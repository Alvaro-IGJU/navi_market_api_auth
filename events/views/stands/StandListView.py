from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from events.models import Stand
from rest_framework.response import Response
from events.serializers import  StandSerializer


class StandListView(APIView):
    """
    Vista para listar todos los stands (Requiere autenticación).
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        stands = Stand.objects.all()
        serializer = StandSerializer(stands, many=True)
        return Response(serializer.data)