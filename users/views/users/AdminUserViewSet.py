from rest_framework import viewsets
from users.permissions import IsSuperUser  
from users.models import User
from users.serializers import (
    UserSerializer,
)

class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperUser]
