from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from users.serializers import (
    RegisterSerializer
)

class UserRegisterView(APIView):
    """
    API para registrar nuevos usuarios.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        print(request.data)  # Verificar datos recibidos
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
        print(serializer.errors)  # Verificar errores
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)