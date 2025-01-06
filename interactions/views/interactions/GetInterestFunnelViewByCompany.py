from django.db.models import Count, Sum, F, Q, Value, IntegerField, ExpressionWrapper, Case, When
from django.db.models.functions import Coalesce
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsCompany
from interactions.models import Interaction
from events.models import Stand


class GetInterestFunnelViewByCompany(APIView):
    """
    Devuelve los datos del embudo de interés de los usuarios
    clasificados como Interés bajo, moderado o alto.
    """
    permission_classes = [IsAuthenticated, IsCompany]

    def get(self, request, company_id):
        try:
            # Verificar si el usuario tiene acceso a la empresa
            user = request.user
            if not user.company_relation or user.company_relation.id != company_id:
                return Response(
                    {"error": "No tienes permiso para acceder aquí."},
                    status=403,
                )

            # Filtrar stands relacionados con la empresa
            stands = Stand.objects.filter(company_id=company_id)

            if not stands.exists():
                return Response(
                    {"error": "No se encontraron stands para esta empresa."},
                    status=404,
                )

            # Obtener todas las interacciones relacionadas
            interactions = Interaction.objects.filter(stand__in=stands)

            # Calcular los puntos por usuario
            user_scores = interactions.values("visit__user_id").annotate(
                # Puntos por tiempo limitado a un máximo de 60 segundos por interacción
                raw_time_points=Coalesce(Sum("interaction_duration"), 0),
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
                ),  # Cada 10 segundos = 1 punto

                # Puntos por otros tipos de interacción
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
            ))

            # Clasificar usuarios por interés
            interest_levels = {
                "Bajo": user_scores.filter(total_points__lte=50).count(),
                "Moderado": user_scores.filter(total_points__gt=50, total_points__lte=100).count(),
                "Alto": user_scores.filter(total_points__gt=100).count(),
            }

            # Estructurar datos del funnel
            funnel_data = [
                {"id": "low_interest", "value": interest_levels["Bajo"], "label": "Interés bajo"},
                {"id": "moderate_interest", "value": interest_levels["Moderado"], "label": "Interés moderado"},
                {"id": "high_interest", "value": interest_levels["Alto"], "label": "Interés alto"},
            ]

            return Response(funnel_data, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
