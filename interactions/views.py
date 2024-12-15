from rest_framework import viewsets
from .models import Visit, Interaction, Lead
from .serializers import VisitSerializer, InteractionSerializer, LeadSerializer
from events.models import Event
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.utils.timezone import now
from rest_framework import status
from events.models import Stand

class RegisterVisitView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, event_id):
        user = request.user
        try:
            # Buscar el evento por su ID
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return Response({'error': 'Evento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        # Crear un nuevo registro de visita para este usuario y evento
        Visit.objects.create(
            user=user,
            event=event,
            time_spent_seconds=0,  # El tiempo será calculado en el cliente u otro flujo
            is_recurrent=False  # Siempre comienza como no recurrente
        )

        return Response({'message': 'Nueva visita registrada con éxito.'}, status=status.HTTP_201_CREATED)


class CloseVisitView(APIView):
    """
    Cierra la visita más reciente de un usuario a un evento.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, event_id):
        user = request.user
        try:
            # Obtener la última visita del usuario al evento
            visit = Visit.objects.filter(user=user, event_id=event_id).order_by('-visit_date').first()
            if not visit:
                return Response({'error': 'No se encontró una visita activa para este evento.'}, status=status.HTTP_404_NOT_FOUND)

            # Calcular el tiempo de la visita
            visit_end_time = now()
            elapsed_time = (visit_end_time - visit.visit_date).total_seconds()
            visit.time_spent_seconds += int(elapsed_time)
            visit.save()

            return Response({'message': 'Visita cerrada correctamente.', 'total_time': visit.time_spent_seconds}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class RegisterInteractionView(APIView):
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

class UpdateInteractionDurationView(APIView):
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