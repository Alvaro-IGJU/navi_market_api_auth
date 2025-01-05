from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from users.serializers import RegisterSerializer
import requests
import pycountry
import os
from email.mime.image import MIMEImage


class UserRegisterView(APIView):
    """
    API para registrar nuevos usuarios.
    """
    permission_classes = [AllowAny]

    def get_country_from_ip(self, ip):
        """Obtiene el país en formato ISO Alpha-3 desde la dirección IP usando ipinfo.io."""
        try:
            response = requests.get(f"https://ipinfo.io/{ip}/json")
            data = response.json()
            country_alpha2 = data.get("country", "Unknown")
            if country_alpha2 != "Unknown":
                country = pycountry.countries.get(alpha_2=country_alpha2)
                return country.alpha_3 if country else "Unknown"
            return "Unknown"
        except Exception as e:
            print(f"Error al obtener el país desde la IP: {e}")
            return "Unknown"

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Obtener la IP del cliente
            ip = request.META.get("HTTP_X_FORWARDED_FOR", request.META.get("REMOTE_ADDR"))
            country_iso_alpha3 = self.get_country_from_ip(ip)
            user.location = country_iso_alpha3
            user.save()

            # Enviar correo electrónico de bienvenida
            subject = "🎉 Bienvenido a Navi Market"
            from_email = settings.EMAIL_HOST_USER
            to_email = [user.email]

            text_content = (
                f"Hola {user.username},\n\n"
                f"Te has registrado correctamente en nuestra plataforma.\n\n"
                f"Saludos,\nEl equipo de Navi Market."
            )

            html_content = f"""
            <html>
            <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; margin: 0; padding: 0;">
                <div style="max-width: 600px; margin: auto; padding: 20px; background-color: #ffffff; border-radius: 10px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);">
                    <h1 style="color: #C7AA68; text-align: center; margin-bottom: 20px;">¡Bienvenido a Navi Market! 🚀</h1>
                    <p style="font-size: 16px; color: #333;">Hola <strong>{user.username}</strong>,</p>
                    <p style="font-size: 16px; color: #333;">
                        Gracias por registrarte en nuestra plataforma. Estamos emocionados de tenerte a bordo.
                    </p>
                    <a href="https://navi-market.com/" style="display: inline-block; padding: 10px 20px; background-color: #C7AA68; color: white; text-decoration: none; border-radius: 5px; font-size: 16px; text-align: center; margin-top: 20px;">Ir a la plataforma</a>
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

            message = EmailMultiAlternatives(subject, text_content, from_email, to_email)
            message.attach_alternative(html_content, "text/html")

            # Adjuntar imagen embebida
            image_path = os.path.join(settings.BASE_DIR, "static/images/logo.png")
            if os.path.exists(image_path):
                with open(image_path, "rb") as img:
                    image = MIMEImage(img.read())
                    image.add_header("Content-ID", "<logo>")
                    message.attach(image)

            try:
                message.send()
            except Exception as e:
                print(f"Error al enviar el correo: {e}")
                return Response(
                    {"message": "Usuario creado, pero no se pudo enviar el correo."},
                    status=status.HTTP_201_CREATED,
                )

            return Response({"message": "Usuario creado exitosamente."}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
