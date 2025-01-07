from django.db.models import Sum, F, Q, Value, IntegerField, CharField, ExpressionWrapper, Case, When, Count
from django.db.models.functions import Coalesce
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsCompany
from interactions.models import Interaction
from events.models import Stand
from users.models import User


class GetCompanyInterestedUsers(APIView):
    """
    Devuelve una lista de usuarios que han interactuado
    con los stands de una empresa específica y calcula su nivel de interés.
    """
    permission_classes = [IsAuthenticated, IsCompany]

    def get(self, request, company_id):
        try:
            # Validar si el usuario pertenece a la compañía
            user = request.user
            if not user.company_relation or user.company_relation.id != company_id:
                return Response(
                    {"error": "No tienes permiso para acceder a esta información."},
                    status=403
                )

            # Obtener los stands de la compañía
            stands = Stand.objects.filter(company_id=company_id)
            if not stands.exists():
                return Response(
                    {"error": "No se encontraron stands para esta empresa."},
                    status=404
                )

            # Obtener las interacciones relacionadas con esos stands
            interactions = Interaction.objects.filter(stand__in=stands)

            # Calcular los puntos de interés por usuario
            user_scores = interactions.values("visit__user_id").annotate(
                time_points=ExpressionWrapper(
                    Coalesce(Sum(
                        Case(
                            When(
                                Q(interaction_type="stand_entry") & Q(interaction_duration__lte=60),
                                then=F("interaction_duration")
                            ),
                            default=Value(60),
                        )
                    ), 0) / Value(10),
                    output_field=IntegerField(),
                ),
                chatbot_points=Count("id", filter=Q(interaction_type="talk_chatbot")) * 5,
                website_points=Count("id", filter=Q(interaction_type="info_pc")) * 15,
                mailbox_points=Count("id", filter=Q(interaction_type="mailbox_click")) * 15,
                video_points=Count("id", filter=Q(interaction_type="show_video")) * 10,
                meeting_points=Count("id", filter=Q(interaction_type="schedule_meeting")) * 40,
                catalog_points=Count("id", filter=Q(interaction_type="download_catalog")) * 15,
            ).annotate(total_points=(
                F("time_points") +
                F("chatbot_points") +
                F("website_points") +
                F("mailbox_points") +
                F("video_points") +
                F("meeting_points") +
                F("catalog_points")
            )).annotate(
                priority=Case(
                    When(
                        Q(meeting_points__gte=40) &
                        Q(website_points__gte=15) &
                        Q(catalog_points__gte=15),
                        then=Value("Decidido")
                    ),
                    When(
                        Q(meeting_points__gte=40) &
                        Q(catalog_points__gte=15),
                        then=Value("Estratégico")
                    ),
                    When(
                        Q(website_points__gte=15) &
                        Q(catalog_points__gte=15),
                        then=Value("Evaluador")
                    ),
                    When(
                        Q(video_points__gte=10) &
                        Q(chatbot_points__gte=5),
                        then=Value("Explorador")
                    ),
                    When(
                        Q(video_points__gte=10) &
                        Q(mailbox_points__gte=15),
                        then=Value("Curioso")
                    ),
                    When(
                        Q(mailbox_points__gte=15),
                        then=Value("Lejano")
                    ),
                    default=Value("Confundido"),
                    output_field=CharField()
                )
            )

            # Obtener información de los usuarios
            user_ids = user_scores.values_list("visit__user_id", flat=True)
            users = User.objects.filter(id__in=user_ids).values(
                "id", "username", "email", "location", "company", "position__title", "sector__name"
            )

            # Combinar información del usuario con sus niveles de interés y prioridades
            response_data = []
            for user in users:
                score_data = user_scores.get(visit__user_id=user["id"])
                response_data.append({
                    "username": user["username"],
                    "email": user["email"] or "Sin email asignado",
                    "location": user["location"] or "Sin ubicación asignada",
                    "company": user["company"] or "Sin empresa asignada",
                    "position_title": user["position__title"] or "Sin posición asignada",
                    "sector_name": user["sector__name"] or "Sin sector asignado",
                    "priority": score_data["priority"],
                    "total_points": score_data["total_points"]
                })

            return Response(response_data, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
