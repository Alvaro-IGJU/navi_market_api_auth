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

            # Calcular los puntos de interés por usuario y ordenar por total_points descendente
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
                interest_level=Case(
                    When(total_points__lte=50, then=Value("Bajo")),
                    When(total_points__gt=50, total_points__lte=100, then=Value("Moderado")),
                    When(total_points__gt=100, then=Value("Alto")),
                    default=Value("Desconocido"),
                    output_field=CharField()
                )
            ).order_by('-total_points')  # Ordenar por puntos descendente

            # Obtener información de los usuarios
            user_ids = user_scores.values_list("visit__user_id", flat=True)
            users = User.objects.filter(id__in=user_ids).values(
                "id", "username", "email", "location", "company", "position__title", "sector__name"
            )

            # Combinar información del usuario con sus niveles de interés
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
                    "interest_level": score_data["interest_level"],
                    "total_points": score_data["total_points"]
                })

            return Response(response_data, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
