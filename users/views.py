from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from rest_framework.viewsets import ReadOnlyModelViewSet
from .permissions import IsSuperUser  
from django.core.mail import send_mail
from .models import User, Position, Sector
from .serializers import (
    LoginSerializer,
    UserSerializer,
    RegisterSerializer,
    ProfileSerializer,
    PositionSerializer,
    SectorSerializer,
)


class PositionViewSet(ReadOnlyModelViewSet):
    """
    ViewSet para listar posiciones ordenadas alfabéticamente.
    """
    queryset = Position.objects.all().order_by('title')  # Ordena por el campo `name`
    serializer_class = PositionSerializer
    permission_classes = [IsAuthenticated]


class SectorViewSet(ReadOnlyModelViewSet):
    """
    ViewSet para listar sectores ordenados alfabéticamente.
    """
    queryset = Sector.objects.all().order_by('name')  # Ordena por el campo `name`
    serializer_class = SectorSerializer
    permission_classes = [IsAuthenticated]


class LoginView(APIView):
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


class RegisterView(APIView):
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


class ProfileView(APIView):
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

class ChangePasswordView(APIView):
    """
    API para cambiar la contraseña del usuario autenticado.
    """
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        data = request.data

        old_password = data.get('old_password')
        new_password = data.get('new_password')

        if not user.check_password(old_password):
            return Response(
                {"detail": "La contraseña actual es incorrecta."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not new_password or len(new_password) < 8:
            return Response(
                {"detail": "La nueva contraseña debe tener al menos 8 caracteres."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()

        return Response(
            {"detail": "Contraseña actualizada correctamente."},
            status=status.HTTP_200_OK
        )

class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperUser]

class AdminPositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = [IsSuperUser]

class AdminSectorViewSet(viewsets.ModelViewSet):
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer
    permission_classes = [IsSuperUser]

class CreateCompanyUserView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        email = request.data.get('email')
        User = get_user_model()

        # Verificar si el usuario ya existe
        if User.objects.filter(email=email).exists():
            return Response({'error': 'El usuario ya existe.'}, status=status.HTTP_409_CONFLICT)

        # Generar un nombre de usuario basado en el email
        username_base = email.split('@')[0]
        username = username_base
        counter = 1

        # Asegurarse de que el username sea único
        while User.objects.filter(username=username).exists():
            username = f"{username_base}{counter}"
            counter += 1

        # Crear usuario con contraseña generada
        password = get_random_string(length=12)
        user = User.objects.create_user(email=email, username=username, password=password, role='Company')

        # Enviar correo electrónico al usuario
        subject = "Bienvenido a nuestra plataforma"
        message = (
            f"Hola {username},\n\n"
            f"Se ha creado una cuenta para ti en nuestra plataforma.\n\n"
            f"Tu nombre de usuario: {username}\n"
            f"Tu contraseña: {password}\n\n"
            f"Por favor, inicia sesión y cambia tu contraseña.\n\n"
            f"Saludos,\nEl equipo de soporte."
        )
        from_email = 'tu_email@gmail.com'  # Cambia por tu dirección de email
        try:
            send_mail(subject, message, from_email, [email])
        except Exception as e:
            return Response(
                {'error': f'Usuario creado, pero no se pudo enviar el correo: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response({
            'message': 'Usuario de empresa creado con éxito. Se ha enviado un correo al usuario.',
        }, status=status.HTTP_201_CREATED)