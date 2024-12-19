from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import  IsAdminUser
from companies.models import Company
from companies.serializers import CompanySerializer


class CompanyAdminDetailView(APIView):
    """
    Vista para que los administradores puedan recuperar, actualizar o eliminar una empresa específica.
    """
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        try:
            company = Company.objects.get(pk=pk)
            serializer = CompanySerializer(company)
            return Response(serializer.data)
        except Company.DoesNotExist:
            return Response({'error': 'Empresa no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            company = Company.objects.get(pk=pk)
            serializer = CompanySerializer(company, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Company.DoesNotExist:
            return Response({'error': 'Empresa no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            company = Company.objects.get(pk=pk)
            company.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Company.DoesNotExist:
            return Response({'error': 'Empresa no encontrada'}, status=status.HTTP_404_NOT_FOUND)
