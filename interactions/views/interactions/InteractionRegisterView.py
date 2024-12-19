from interactions.models import Visit, Interaction
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.timezone import now
from rest_framework import status
from events.models import Stand

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
            interaction = Interaction.objects.create(
                visit=visit,
                stand=stand,
                interaction_type=request.data.get("interaction_type"),
            )

            return Response(
                {"interaction_id": interaction.id},
                status=status.HTTP_201_CREATED,
            )
        except Stand.DoesNotExist:
            return Response(
                {"error": "Stand not found"}, status=status.HTTP_404_NOT_FOUND
            )