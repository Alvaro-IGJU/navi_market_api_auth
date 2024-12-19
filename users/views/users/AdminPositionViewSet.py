from rest_framework import viewsets
from users.permissions import IsSuperUser  
from users.models import Position
from users.serializers import (
    PositionSerializer,
)

class AdminPositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = [IsSuperUser]