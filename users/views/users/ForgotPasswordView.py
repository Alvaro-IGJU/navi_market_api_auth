from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage
from django.conf import settings
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models import PasswordResetToken, User
from users.serializers import ForgotPasswordSerializer
import os


class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                # Verificar si el usuario existe
                if not User.objects.filter(email=email).exists():
                    return Response({'error': 'El correo no está registrado.'}, status=status.HTTP_404_NOT_FOUND)
                
                user = User.objects.get(email=email)

                # Crear un token de recuperación para el usuario
                token = PasswordResetToken.objects.create(user=user)
                
                # Crear el enlace de recuperación
                reset_url = f"http://localhost:3000/reset-password/{token.token}/"

                # Contenido del correo (Texto y HTML)
                subject = "Recuperación de contraseña"
                from_email = settings.EMAIL_HOST_USER
                to_email = [email]

                text_content = (
                    f"Hola {user.username},\n\n"
                    f"Recibimos una solicitud para restablecer tu contraseña. "
                    f"Usa el siguiente enlace para restablecerla:\n"
                    f"{reset_url}\n\n"
                    f"Si no solicitaste este cambio, ignora este correo.\n\n"
                    f"Saludos,\nEl equipo de soporte."
                )

                html_content = f"""
                <html>
                <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; margin: 0; padding: 0;">
                    <div style="max-width: 600px; margin: auto; padding: 20px; background-color: #ffffff; border-radius: 10px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);">
                        <h1 style="color: #C7AA68; text-align: center; margin-bottom: 20px;">Recupera tu contraseña 🚀</h1>
                        <p style="font-size: 16px; color: #333;">Hola <strong>{user.username}</strong>,</p>
                        <p style="font-size: 16px; color: #333;">
                            Hemos recibido una solicitud para restablecer tu contraseña. Si fuiste tú, por favor usa el siguiente enlace:
                        </p>
                        <div style="background-color: #f4f4f4; padding: 15px; border-radius: 5px; margin: 20px 0;">
                            <p style="font-size: 14px; color: #555;"><strong>Enlace para restablecer tu contraseña:</strong></p>
                            <p style="font-size: 14px; color: #555;">
                                <a href="{reset_url}" style="color: #C7AA68; text-decoration: none;">Restablecer mi contraseña</a>
                            </p>
                        </div>
                        <p style="font-size: 16px; color: #333;">
                            Si no realizaste esta solicitud, puedes ignorar este mensaje.
                        </p>
                        <p style="font-size: 14px; color: #999; text-align: center; margin-top: 30px;">
                            Si tienes alguna pregunta, no dudes en <a href="https://navi-market.com/contact" style="color: #C7AA68; text-decoration: none;">contactarnos</a>.
                        </p>
                        <p style="font-size: 14px; color: #999; text-align: center; margin-top: 10px;">
                            Gracias por confiar en Navi Market. 💛
                        </p>
                    </div>
                </body>
                </html>
                """
                
                # Crear el mensaje de correo
                message = EmailMultiAlternatives(subject, text_content, from_email, to_email)
                message.attach_alternative(html_content, "text/html")

                # Adjuntar la imagen embebida (como ejemplo logo)
                image_path = os.path.join(settings.BASE_DIR, "static/images/logo.png")  # Ruta a la imagen
                if os.path.exists(image_path):
                    with open(image_path, "rb") as img:
                        image = MIMEImage(img.read())
                        image.add_header("Content-ID", "<logo>")
                        message.attach(image)

                # Intentar enviar el correo
                try:
                    message.send()
                    return Response({"message": "Correo de recuperación enviado."}, status=status.HTTP_200_OK)
                except Exception as e:
                    return Response(
                        {'error': f'Hubo un error al enviar el correo: {str(e)}'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
                
            except Exception:
                return Response({"message": "Correo no registrado."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
