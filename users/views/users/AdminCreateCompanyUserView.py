from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.permissions import IsSuperUser
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from companies.models import Company
import os


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

        # Crear una empresa asociada al usuario
        company = Company.objects.create(
            name=f"Empresa de {username}",  # Nombre genérico
            contact_email=email,
            description=f"Descripción de la empresa de {username}.",
        )

        # Asignar la empresa al usuario
        user.company_relation = company
        user.save()

        # Enviar correo electrónico al usuario con imagen
        subject = "🎉 Bienvenido a Navi Market"
        from_email = settings.EMAIL_HOST_USER
        to_email = [email]

        text_content = (
            f"Hola {username},\n\n"
            f"Se ha creado una cuenta para ti en nuestra plataforma.\n\n"
            f"Tu nombre de usuario: {username}\n"
            f"Tu contraseña: {password}\n\n"
            f"Por favor, inicia sesión y cambia tu contraseña.\n\n"
            f"Saludos,\nEl equipo de soporte."
        )

        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; margin: 0; padding: 0;">
            <div style="max-width: 600px; margin: auto; padding: 20px; background-color: #ffffff; border-radius: 10px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);">
                <h1 style="color: #C7AA68; text-align: center; margin-bottom: 20px;">¡Bienvenido a Navi Market! 🚀</h1>
                <p style="font-size: 16px; color: #333;">Hola <strong>{username}</strong>,</p>
                <p style="font-size: 16px; color: #333;">
                    Nos alegra que te hayas unido a nuestra plataforma. Hemos creado una cuenta para ti para que puedas empezar a disfrutar de nuestros servicios.
                </p>
                <div style="background-color: #f4f4f4; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <p style="font-size: 14px; color: #555;"><strong>Tu nombre de usuario:</strong> {username}</p>
                    <p style="font-size: 14px; color: #555;"><strong>Tu contraseña:</strong> {password}</p>
                </div>
                <p style="font-size: 16px; color: #333;">
                    Por favor, inicia sesión en tu cuenta y recuerda cambiar tu contraseña por una que solo tú conozcas.
                </p>
                <a href="https://navifairs.com/" style="display: inline-block; padding: 10px 20px; background-color: #C7AA68; color: white; text-decoration: none; border-radius: 5px; font-size: 16px; text-align: center; margin-top: 20px;">Iniciar sesión</a>
                <p style="font-size: 14px; color: #999; text-align: center; margin-top: 30px;">
                    Si tienes alguna pregunta, no dudes en <a href="https://navifairs.com/contact" style="color: #C7AA68; text-decoration: none;">contactarnos</a>.
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

        # Adjuntar la imagen embebida
        image_path = os.path.join(settings.BASE_DIR, "static/images/logo.png")  # Ruta a la imagen
        if os.path.exists(image_path):
            with open(image_path, "rb") as img:
                image = MIMEImage(img.read())
                image.add_header("Content-ID", "<logo>")
                message.attach(image)

        try:
            message.send()
        except Exception as e:
            return Response(
                {'error': f'Usuario creado y empresa asociada, pero no se pudo enviar el correo: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response({
            'message': 'Usuario de empresa creado con éxito.',
        }, status=status.HTTP_201_CREATED)