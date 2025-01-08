from interactions.models import Interaction
from users.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsCompany
from django.db.models import F
from rest_framework import status


class UsersScheduledMeetingView(APIView):
    """
    Devuelve los usuarios que han intentado hacer un schedule meeting.
    """
    permission_classes = [IsAuthenticated, IsCompany]

    def get(self, request, company_id):
        try:
            # Filtrar interacciones del tipo "schedule_meeting"
            interactions = Interaction.objects.filter(
                interaction_type="schedule_meeting",
                stand__company_id=company_id
            ).select_related("visit__user").distinct()

            # Obtener los usuarios únicos
            users = User.objects.filter(
                id__in=interactions.values_list("visit__user_id", flat=True)
            ).values(
                "id", "username", "email", "location", "company", "position__title", "profile_picture"
            )

            response_data = [
                {
                    "id": user["id"],
                    "username": user["username"],
                    "email": user.get("email", "Sin email asignado"),
                    "location": user.get("location", "Sin ubicación asignada"),
                    "company": user.get("company", "Sin empresa asignada"),
                    "position": user.get("position__title", "Sin posición asignada"),
                    "profile_picture": user.get("profile_picture", "Sin imagen asignada"),
                }
                for user in users
            ]

            return Response({
                "total": len(response_data),
                "users": response_data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
