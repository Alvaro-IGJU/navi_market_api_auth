from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from companies.models import Company
from companies.serializers import CompanySerializer

class CompanyAdminListView(APIView):
    """
    Vista para que los administradores puedan listar todas las empresas.
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data)
