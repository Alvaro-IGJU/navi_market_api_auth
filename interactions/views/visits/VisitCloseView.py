from interactions.models import Visit
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.utils.timezone import now
from rest_framework import status

class VisitCloseView(APIView):
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