from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from users.models import PasswordResetToken  # Asumiendo que tienes este modelo de token de restablecimiento de contraseña
from rest_framework.permissions import AllowAny

User = get_user_model()

class ResetPasswordView(APIView):
    """
    View to handle password reset using a token.
    """
    permission_classes = [AllowAny]

    def post(self, request, token):
        try:
            # Verificar si el token existe
            reset_token = PasswordResetToken.objects.filter(token=token).first()
            
            if not reset_token:
                return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

            # Obtener el usuario usando el token
            user = reset_token.user

            # Obtener la nueva contraseña del request
            new_password = request.data.get('password')

            if not new_password:
                return Response({"error": "Password is required."}, status=status.HTTP_400_BAD_REQUEST)

            # Cambiar la contraseña del usuario
            user.set_password(new_password)
            user.save()

            # Marcar el token como usado o eliminarlo (si es necesario)
            reset_token.delete()

            return Response({"message": "Password has been successfully reset."}, status=status.HTTP_200_OK)
        
        except Exception as e:
            # Manejar cualquier excepción
            return Response({"error": "An error occurred while processing the request."}, status=status.HTTP_400_BAD_REQUEST)
