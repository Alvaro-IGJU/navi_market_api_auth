from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import PasswordResetToken  # Modelo para manejar tokens de restablecimiento
from rest_framework.permissions import AllowAny

class VerifyTokenView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, token):
        try:
            # Verificar si el token existe en la base de datos
            reset_token = PasswordResetToken.objects.filter(token=token).first()

            if reset_token is None:
                # Si el token no existe o ha expirado, redirigir al usuario a /auth
                return Response({"error": "Token inválido o expirado. Por favor, solicite uno nuevo."}, status=status.HTTP_400_BAD_REQUEST)

            # Si el token es válido, puedes continuar con el flujo
            return Response({"message": "Token válido. Ahora puedes restablecer tu contraseña."}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": "Hubo un error al verificar el token."}, status=status.HTTP_400_BAD_REQUEST)
