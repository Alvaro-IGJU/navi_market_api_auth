from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsCompany
from rest_framework.response import Response
from rest_framework import status
from companies.models import Company
from companies.serializers import CompanySerializer

class GetCompanyDetails(APIView):
    """
    View para obtener los detalles de una empresa específica.
    """

    permission_classes = [IsAuthenticated, IsCompany]

    def get(self, request, company_id):
        try:
            # Obtener la empresa por su ID
            company = Company.objects.get(pk=company_id)

            # Verificar si el usuario es el dueño de la empresa
            if company.id != request.user.company_relation.id:
                return Response(
                    {"error": "No tienes permiso para acceder a esta empresa."},
                    status=status.HTTP_403_FORBIDDEN
                )

            # Serializar los datos de la empresa
            serializer = CompanySerializer(company)

            # Devolver la respuesta
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Company.DoesNotExist:
            return Response(
                {"error": "Empresa no encontrada."}, status=status.HTTP_404_NOT_FOUND
            )
