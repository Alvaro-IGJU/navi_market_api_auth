from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet
from users.models import Position
from users.serializers import (
    PositionSerializer,
)


class PositionViewSet(ReadOnlyModelViewSet):
    """
    ViewSet para listar posiciones ordenadas alfabéticamente.
    """
    queryset = Position.objects.all().order_by('title')  # Ordena por el campo `name`
    serializer_class = PositionSerializer
    permission_classes = [IsAuthenticated]
