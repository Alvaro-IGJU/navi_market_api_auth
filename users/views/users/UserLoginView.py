from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from users.serializers import (
    LoginSerializer
)

class UserLoginView(APIView):
    """
    API para iniciar sesión.
    """
    permission_classes = [AllowAny]  # Permitir acceso sin autenticación

    def post(self, request):
        print(request.data)  # Verificar datos recibidos

        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
