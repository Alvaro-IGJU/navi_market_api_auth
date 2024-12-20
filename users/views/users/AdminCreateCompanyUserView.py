from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.permissions import IsSuperUser
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from companies.models import Company


class AdminCreateCompanyUserView(APIView):
    permission_classes = [IsSuperUser]

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
        print(password)
        # Crear una empresa asociada al usuario
        company = Company.objects.create(
            name=f"Empresa de {username}",  # Nombre genérico
            contact_email=email,
            description=f"Descripción de la empresa de {username}.",
        )
        # Asignar la empresa al usuario
        user.company_relation = company
        user.save()

        # Enviar correo electrónico al usuario (comentar esta parte temporalmente)
        subject = "Bienvenido a nuestra plataforma"
        message = (
            f"Hola {username},\n\n"
            f"Se ha creado una cuenta para ti en nuestra plataforma.\n\n"
            f"Tu nombre de usuario: {username}\n"
            f"Tu contraseña: {password}\n\n"
            f"Por favor, inicia sesión y cambia tu contraseña.\n\n"
            f"Saludos,\nEl equipo de soporte."
        )
        from_email = 'navi-market@gmail.com'  # Cambia por tu dirección de email
        try:
            send_mail(subject, message, from_email, [email])
        except Exception as e:
            return Response(
                {'error': f'Usuario creado y empresa asociada, pero no se pudo enviar el correo: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response({
            'message': f'Usuario de empresa creado con éxito.',
        }, status=status.HTTP_201_CREATED)