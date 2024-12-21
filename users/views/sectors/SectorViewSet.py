from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet
from users.models import Sector
from users.serializers import (
    SectorSerializer,
)

class SectorViewSet(ReadOnlyModelViewSet):
    """
    ViewSet para listar sectores ordenados alfabéticamente.
    """
    queryset = Sector.objects.all().order_by('name')  # Ordena por el campo `name`
    serializer_class = SectorSerializer
    permission_classes = [AllowAny]
