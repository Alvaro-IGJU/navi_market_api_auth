from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsCompany
from interactions.models import Interaction
from events.models import Stand
from users.models import User
from django.db.models import Count

class InteractionCompanyUserSectorsView(APIView):
    """
    Devuelve los sectores de los usuarios que han interactuado
    con los stands de una empresa específica.
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

            print(f"Usuario autenticado: {user.email} - Empresa ID: {company_id}")

            # Obtener los stands de la compañía
            stands = Stand.objects.filter(company_id=company_id)
            if not stands.exists():
                print("No se encontraron stands para esta empresa.")
                return Response(
                    {"error": "No se encontraron stands para esta empresa."},
                    status=404
                )
            print("STANDS:")
            for stand in stands:
                print(stand)

            # Obtener las interacciones relacionadas con esos stands
            interactions = Interaction.objects.filter(stand__in=stands).select_related('visit__user')
            print("INTERACTIONS:")
            for interaction in interactions:
                print(interaction)

            # Obtener los IDs de los usuarios que interactuaron
            user_ids = interactions.values_list('visit__user_id', flat=True).distinct()
            if not user_ids:
                print("No se encontraron usuarios que interactuaron.")
                return Response([], status=200)

            print(f"USERS ID LIST: {list(user_ids)}")

            # Contar sectores de los usuarios
            users_with_sectors = User.objects.filter(id__in=user_ids).exclude(sector__name__isnull=True)
            print("USERS WITH SECTORS:")
            for user in users_with_sectors:
                print(user)

            sector_data = (
                users_with_sectors
                .values("sector__name")
                .annotate(user_count=Count("id"))
            )

            print("SECTOR DATA:")
            for sector in sector_data:
                print(sector)

            # Formatear los datos para el frontend
            response_data = [
                {
                    "sector_name": item["sector__name"],
                    "user_count": item["user_count"]
                }
                for item in sector_data
            ]

            print(f"FINAL RESPONSE DATA: {response_data}")
            return Response(response_data, status=200)

        except Exception as e:
            print(f"ERROR: {str(e)}")
            return Response({"error": str(e)}, status=500)
