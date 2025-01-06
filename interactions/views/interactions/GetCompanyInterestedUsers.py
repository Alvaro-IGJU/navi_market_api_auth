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

            # Obtener los stands de la compañía
            stands = Stand.objects.filter(company_id=company_id)
            if not stands.exists():
                return Response(
                    {"error": "No se encontraron stands para esta empresa."},
                    status=404
                )

            # Obtener las interacciones relacionadas con esos stands
            interactions = Interaction.objects.filter(stand__in=stands).select_related('visit__user')

            # Obtener los IDs de los usuarios que interactuaron
            user_ids = interactions.values_list('visit__user_id', flat=True).distinct()
            if not user_ids:
                return Response([], status=200)

            # Obtener información de los usuarios interesados
            interested_users = User.objects.filter(id__in=user_ids).values(
                "username", "email", "location", "company", "position__title", "sector__name", 
            )
            # Formatear los datos para el frontend
            response_data = [
                {
                    "username": user["username"],
                    "email": user["email"] or "Sin email asignado",
                    "location": user["location"] or "Sin ubicación asignada",
                    "company": user["company"] or "Sin empresa asignada",
                    "position_title": user["position__title"] or "Sin posición asignada",
                    "sector_name": user["sector__name"] or "Sin sector asignado"
                }
                for user in interested_users
            ]

            return Response(response_data, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
