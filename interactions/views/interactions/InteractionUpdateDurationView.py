from interactions.models import Interaction
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.timezone import now
from rest_framework import status
from decimal import Decimal

class InteractionUpdateDurationView(APIView):
    def post(self, request, interaction_id):
        try:
            interaction = Interaction.objects.get(id=interaction_id)
            duration = request.data.get("duration", 0)

            if not isinstance(duration, (int, float, str)):
                return Response(
                    {"error": "Invalid duration type. Must be a number."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Convertir la duración a Decimal
            duration_decimal = Decimal(str(duration))

            # Sumar la duración al valor existente
            interaction.interaction_duration += duration_decimal
            interaction.save()

            return Response(
                {"message": "Duration updated successfully"},
                status=status.HTTP_200_OK,
            )
        except Interaction.DoesNotExist:
            return Response(
                {"error": "Interaction not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
