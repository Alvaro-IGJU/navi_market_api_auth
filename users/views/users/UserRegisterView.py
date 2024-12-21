from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from users.serializers import RegisterSerializer
import requests
import pycountry  # Asegúrate de instalar pycountry: pip install pycountry

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
            # response = requests.get(f"https://ipinfo.io/103.121.48.255/json")
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

    def post(self, request):
        print(request.data)  # Verificar datos recibidos
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Obtener la IP del cliente
            ip = request.META.get("HTTP_X_FORWARDED_FOR")
            if ip:
                ip = ip.split(",")[0]  # Usar la primera IP en caso de múltiples proxies
            else:
                ip = request.META.get("REMOTE_ADDR")
            print(f"IP del usuario: {ip}")

            # Obtener la ubicación del país desde la IP
            country_iso_alpha3 = self.get_country_from_ip(ip)
            print(f"País detectado (Alpha-3): {country_iso_alpha3}")

            # Guardar el país en el campo 'location' del usuario
            user.location = country_iso_alpha3
            user.save()

            return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
        print(serializer.errors)  # Verificar errores
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
