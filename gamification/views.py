from rest_framework import viewsets
from .models import GamificationActivity
from .serializers import GamificationActivitySerializer

class GamificationActivityViewSet(viewsets.ModelViewSet):
    queryset = GamificationActivity.objects.all()
    serializer_class = GamificationActivitySerializer
