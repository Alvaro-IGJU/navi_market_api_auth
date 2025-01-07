from django.db.models import Count, Q, Value, Case, When, IntegerField
from django.db.models.functions import Coalesce
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsCompany
from interactions.models import Interaction
from events.models import Stand


class GetInterestFunnelViewByCompany(APIView):
    """
    Devuelve la cantidad de usuarios clasificados por nivel de interés.
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

            # Verificar las condiciones de cada usuario
            user_scores = interactions.values("visit__user_id").annotate(
                has_schedule_meeting=Count("id", filter=Q(interaction_type="schedule_meeting")),
                has_info_pc=Count("id", filter=Q(interaction_type="info_pc")),
                has_download_catalog=Count("id", filter=Q(interaction_type="download_catalog")),
                has_show_video=Count("id", filter=Q(interaction_type="show_video")),
                has_talk_chatbot=Count("id", filter=Q(interaction_type="talk_chatbot")),
                has_mailbox=Count("id", filter=Q(interaction_type="mailbox")),
            ).annotate(
                level=Case(
                    # Usuarios Decididos
                    When(
                        Q(has_schedule_meeting__gte=1) &
                        Q(has_info_pc__gte=1) &
                        Q(has_download_catalog__gte=1),
                        then=Value(1)
                    ),
                    # Usuarios Estratégicos
                    When(
                        Q(has_schedule_meeting__gte=1) &
                        Q(has_download_catalog__gte=1),
                        then=Value(2)
                    ),
                    # Usuarios Evaluadores
                    When(
                        Q(has_info_pc__gte=1) &
                        Q(has_download_catalog__gte=1),
                        then=Value(3)
                    ),
                    # Usuarios Exploradores
                    When(
                        Q(has_show_video__gte=1) &
                        Q(has_talk_chatbot__gte=1),
                        then=Value(4)
                    ),
                    # Usuarios Curiosos
                    When(
                        Q(has_show_video__gte=1) &
                        Q(has_mailbox__gte=1),
                        then=Value(5)
                    ),
                    # Usuarios Lejanos
                    When(
                        Q(has_mailbox__gte=1),
                        then=Value(6)
                    ),
                    # Usuarios Confundidos
                    default=Value(7),
                    output_field=IntegerField()
                )
            )

            # Contar usuarios por nivel
            levels = {}
            for user in user_scores:
                level = user["level"]
                levels[level] = levels.get(level, 0) + 1

            # Formatear los datos
            formatted_data = [
                {
                    "level": level,
                    "category": self.get_category(level),
                    "count": count,
                }
                for level, count in sorted(levels.items())
            ]

            return Response(formatted_data, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)

    @staticmethod
    def get_category(level):
        categories = {
            1: "Usuarios Decididos",
            2: "Usuarios Estratégicos",
            3: "Usuarios Evaluadores",
            4: "Usuarios Exploradores",
            5: "Usuarios Curiosos",
            6: "Usuarios Lejanos",
            7: "Usuarios Confundidos",
        }
        return categories.get(level, "Desconocido")
