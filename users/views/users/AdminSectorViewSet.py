from rest_framework import viewsets
from users.permissions import IsSuperUser  
from users.models import Sector
from users.serializers import (
    SectorSerializer,
)
class AdminSectorViewSet(viewsets.ModelViewSet):
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer
    permission_classes = [IsSuperUser]
