from interactions.models import Visit, Interaction
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.timezone import now
from rest_framework import status
from events.models import Stand
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

class InteractionRegisterView(APIView):
    def post(self, request, stand_id):
        try:
            user = request.user
            stand = Stand.objects.get(id=stand_id)

            # Intentar obtener una visita activa o crear una nueva
            visit = Visit.objects.filter(user=user, event=stand.event).order_by("-visit_date").first()

            if not visit:
                visit = Visit.objects.create(user=user, event=stand.event)

            # Registrar interacción
            interaction_type = request.data.get("interaction_type")
            status_value = "pending" if interaction_type == "schedule_meeting" else None
            interaction = Interaction.objects.create(
                visit=visit,
                stand=stand,
                interaction_type=interaction_type,
                status=status_value  # Asignar "pending" solo para "schedule_meeting"
            )   
          

                

            # Si la interacción es de tipo "mailbox", enviar un correo electrónico
            if interaction_type == "mailbox":
                company = stand.company  # Suponiendo que `stand` está asociado con una empresa
                subject = f"Información de {company.name}"
                from_email = settings.EMAIL_HOST_USER
                to_email = [user.email]

                text_content = (
                    f"Hola {user.username},\n\n"
                    f"Gracias por interactuar con el buzón de {company.name}.\n\n"
                    f"Aquí tienes más información sobre la empresa:\n\n"
                    f"Nombre: {company.name}\n"
                    f"Descripción: {company.description}\n\n"
                    f"Si tienes alguna pregunta, no dudes en contactarnos.\n\n"
                    f"Saludos,\nEl equipo de Navi Fairs."
                )

                html_content = f"""
                <html>
                <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; margin: 0; padding: 0;">
                    <div style="max-width: 600px; margin: auto; padding: 20px; background-color: #ffffff; border-radius: 10px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);">
                        <h1 style="color: #C7AA68; text-align: center; margin-bottom: 20px;">Información de {company.name}</h1>
                        <p style="font-size: 16px; color: #333;">Hola <strong>{user.username}</strong>,</p>
                        <p style="font-size: 16px; color: #333;">
                            Gracias por interactuar con el buzón de <strong>{company.name}</strong>.
                        </p>
                        <div style="background-color: #f4f4f4; padding: 15px; border-radius: 5px; margin: 20px 0;">
                            <p style="font-size: 14px; color: #555;"><strong>Descripción:</strong> {company.description}</p>
                        </div>
                        <p style="font-size: 16px; color: #333;">
                            Si tienes alguna pregunta, no dudes en contactarnos.
                        </p>
                        <p style="font-size: 14px; color: #999; text-align: center; margin-top: 30px;">
                            Gracias por confiar en Navi Fairs. 💛
                        </p>
                    </div>
                </body>
                </html>
                """
                message = EmailMultiAlternatives(subject, text_content, from_email, to_email)
                message.attach_alternative(html_content, "text/html")
                try:
                    message.send()
                except Exception as e:
                    return Response(
                        {"error": f"Interacción registrada, pero no se pudo enviar el correo: {str(e)}"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

            return Response(
                {"interaction_id": interaction.id},
                status=status.HTTP_201_CREATED,
            )
        except Stand.DoesNotExist:
            return Response(
                {"error": "Stand not found"}, status=status.HTTP_404_NOT_FOUND
            )
