from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from users.serializers import RegisterSerializer
import requests
import pycountry  # Asegúrate de instalar pycountry: pip install pycountry
from django.conf import settings

class UserRegisterView(APIView):
    """
    API para registrar nuevos usuarios.
    """
    permission_classes = [AllowAny]

    def get_country_from_ip(self, ip):
        """Obtiene el país en formato ISO Alpha-3 desde la dirección IP usando ipinfo.io."""
        try:
            # Realiza la solicitud a ipinfo.io
            response = requests.get(f"https://ipinfo.io/{ip}/json")
            data = response.json()
            country_alpha2 = data.get("country", "Unknown")  # Código ISO Alpha-2 (como "US")
            
            # Convertir Alpha-2 a Alpha-3 usando pycountry
            if country_alpha2 != "Unknown":
                country = pycountry.countries.get(alpha_2=country_alpha2)
                return country.alpha_3 if country else "Unknown"
            return "Unknown"
        except Exception as e:
            print(f"Error al obtener el país desde la IP: {e}")
            return "Unknown"

    def send_welcome_email(self, user):
        """Envía un correo de bienvenida al nuevo usuario."""
        subject = "Bienvenido a Nuestra Plataforma"
        message = f"""
        Hola {user.username},

        ¡Gracias por registrarte en nuestra plataforma! Nos alegra tenerte aquí.

        Si tienes alguna pregunta o necesitas ayuda, no dudes en contactarnos.

        Saludos cordiales,
        El equipo de nuestra plataforma
        """
        from_email = settings.DEFAULT_FROM_EMAIL  # Asegúrate de configurar esto en settings.py
        recipient_list = [user.email]
        
        try:
            send_mail(subject, message, from_email, recipient_list)
            print(f"Correo de bienvenida enviado a {user.email}")
        except Exception as e:
            print(f"Error al enviar el correo de bienvenida: {e}")

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Obtener la IP del cliente
            ip = request.META.get("HTTP_X_FORWARDED_FOR")
            if ip:
                ip = ip.split(",")[0]  # Usar la primera IP en caso de múltiples proxies
            else:
                ip = request.META.get("REMOTE_ADDR")

            # Obtener la ubicación del país desde la IP
            country_iso_alpha3 = self.get_country_from_ip(ip)
            user.location = country_iso_alpha3
            user.save()

            # Enviar correo de bienvenida
            self.send_welcome_email(user)

            return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
