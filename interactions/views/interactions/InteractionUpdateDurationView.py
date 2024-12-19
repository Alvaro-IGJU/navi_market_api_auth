from interactions.models import Interaction
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.timezone import now
from rest_framework import status

class InteractionUpdateDurationView(APIView):
    def post(self, request, interaction_id):
        try:
            interaction = Interaction.objects.get(id=interaction_id)
            duration = request.data.get("duration", 0)
            interaction.interaction_duration += duration
            interaction.save()

            return Response(
                {"message": "Duration updated successfully"},
                status=status.HTTP_200_OK,
            )
        except Interaction.DoesNotExist:
            return Response(
                {"error": "Interaction not found"}, status=status.HTTP_404_NOT_FOUND
            )
