from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsCompany
from users.models import User
from interactions.models import Interaction
from events.models import Stand
from django.db.models import Count

class InteractionUsersLocationView(APIView):
    """
    Devuelve los usuarios únicos que han interactuado con los stands
    de una empresa específica, agrupados por ubicación.
    """
    permission_classes = [IsAuthenticated, IsCompany]

    def get(self, request, company_id):
        try:
            # Validar si el usuario pertenece a la compañía
            user = request.user
            if not user.company_relation or user.company_relation.id != company_id:
                return Response(
                    {"error": "No tienes permiso para acceder aquí."},
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
            interactions = Interaction.objects.filter(stand__in=stands).select_related('visit__user')

            # Obtener usuarios únicos que han interactuado
            user_ids = interactions.values_list('visit__user_id', flat=True).distinct()
            users = User.objects.filter(id__in=user_ids)

            # Agrupar por ubicación y contar usuarios
            location_data = (
                users.values("location")
                .annotate(value=Count("id"))
                .exclude(location__isnull=True)
                .exclude(location="")
            )

            # Imprime el resultado final antes de devolverlo
            response_data = [{"id": loc["location"], "value": loc["value"]} for loc in location_data]

            return Response(response_data, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
