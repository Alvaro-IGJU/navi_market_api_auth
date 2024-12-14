from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Company
from .serializers import CompanySerializer

class CompanyViewSet(ModelViewSet):
    """
    ViewSet para manejar las operaciones CRUD del modelo Company.
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if self.action in ['list', 'retrieve']:
            if user.company:
                return Company.objects.filter(id=user.company.id)
            return Company.objects.none()
        return Company.objects.all()

    def perform_create(self, serializer):
        company = serializer.save()
        self.request.user.company_relation = company
        self.request.user.save()

    def perform_update(self, serializer):
        if self.request.user.company:
            serializer.save()
