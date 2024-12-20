from interactions.models import Interaction
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsCompany
from rest_framework.views import APIView
from rest_framework import status
from events.models import Stand
from django.db.models import Count, Sum

class InteractionCompaniesView(APIView):
    """
    Devuelve las interacciones realizadas en los stands de una empresa específica,
    tanto el total como por cada stand.
    """
    permission_classes = [IsAuthenticated, IsCompany]

    def get(self, request, company_id):
        try:
            # Filtrar los stands por empresa
            stands = Stand.objects.filter(company_id=company_id)

            if not stands.exists():
                return Response(
                    {"error": "No se encontraron stands para esta empresa."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Obtener todas las interacciones relacionadas con estos stands
            interactions = Interaction.objects.filter(stand__in=stands)

            # Resumen general de interacciones por tipo
            interaction_summary = interactions.values("interaction_type").annotate(
                total_interactions=Count("id"),
                total_duration=Sum("interaction_duration")
            )

            # Datos específicos por stand
            stands_data = []
            for stand in stands:
                stand_interactions = interactions.filter(stand=stand).values("interaction_type").annotate(
                    total_interactions=Count("id"),
                    total_duration=Sum("interaction_duration")
                )
                stands_data.append({
                    "stand_id": stand.id,
                    "stand_name": stand.name,
                    "event_name": stand.event.name,  # Incluye el nombre del evento del stand
                    "total_interactions": sum([item["total_interactions"] for item in stand_interactions]),
                    "interaction_details": list(stand_interactions),
                })

            # Estructura de respuesta
            response_data = {
                "company_id": company_id,
                "total_interactions": interactions.count(),
                "interaction_details": list(interaction_summary),  # Resumen global
                "stands_details": stands_data,  # Interacciones por stand
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

