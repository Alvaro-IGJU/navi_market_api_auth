from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import CompanySerializer


class OwnerCompanyDetailView(APIView):
    """
    Vista para que el dueño de una empresa pueda recuperar o actualizar los datos de su empresa.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Verifica si el usuario tiene una relación con alguna empresa
        if not request.user.company_relation:
            return Response({'error': 'No tienes una empresa asociada.'}, status=status.HTTP_404_NOT_FOUND)

        # Recupera la empresa asociada
        company = request.user.company_relation
        serializer = CompanySerializer(company)
        return Response(serializer.data)

    def put(self, request):
        # Verifica si el usuario tiene una relación con alguna empresa
        if not request.user.company_relation:
            return Response({'error': 'No tienes una empresa asociada.'}, status=status.HTTP_404_NOT_FOUND)

        # Recupera la empresa asociada
        company = request.user.company_relation
        print(request.data)
        serializer = CompanySerializer(company, data=request.data, partial=True)  # Permite actualizaciones parciales
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
