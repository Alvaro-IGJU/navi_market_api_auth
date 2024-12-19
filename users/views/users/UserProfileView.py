from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from users.serializers import (
    ProfileSerializer,
)
class UserProfileView(APIView):
    """
    API para obtener y actualizar datos del perfil del usuario autenticado.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        data = request.data
        print("Datos recibidos:", data)

        # Convertir valores vacíos o nulos a None
        if 'position' in data:
            if data['position'] in ["", None]:
                data['position'] = None
            elif isinstance(data['position'], str):
                try:
                    data['position'] = int(data['position'])
                except ValueError:
                    return Response(
                        {"position": "El valor de position debe ser un número válido."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

        if 'sector' in data:
            if data['sector'] in ["", None]:
                data['sector'] = None
            elif isinstance(data['sector'], str):
                try:
                    data['sector'] = int(data['sector'])
                except ValueError:
                    return Response(
                        {"sector": "El valor de sector debe ser un número válido."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

        # Serializar y guardar los datos
        serializer = ProfileSerializer(request.user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            print("Usuario actualizado:", serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        print("Errores del serializador:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)