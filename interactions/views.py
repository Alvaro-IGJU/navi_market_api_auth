from rest_framework import viewsets
from .models import Visit, Interaction, Lead
from .serializers import VisitSerializer, InteractionSerializer, LeadSerializer
from events.models import Event
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.utils.timezone import now
from rest_framework import status


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



class InteractionViewSet(viewsets.ModelViewSet):
    queryset = Interaction.objects.all()
    serializer_class = InteractionSerializer

class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
