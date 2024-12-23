from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from events.models import Event
from events.serializers import EventSerializer
from rest_framework.response import Response


class EventRetrieveView(APIView):
    """
    Vista para obtener los detalles de un evento específico (Acceso público).
    Devuelve la información del evento junto con los sectores únicos de las empresas participantes.
    """
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            # Obtener el evento específico
            event = Event.objects.get(pk=pk)

            # Serializar los detalles del evento
            serializer = EventSerializer(event)

            # Obtener los sectores únicos de las empresas asociadas a través de stands
            stands = event.stands.all()  # Asume que hay una relación stands en Event
            companies = [stand.company for stand in stands if stand.company]
            print(companies, "AAAAAAAAAAAA")
            sectors = {company.sector.name for company in companies if company.sector and company.sector}

            # Formar la respuesta combinada
            response_data = {
                "event": serializer.data,
                "unique_sectors": list(sectors),
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Event.DoesNotExist:
            return Response(
                {"error": "Evento no encontrado"}, status=status.HTTP_404_NOT_FOUND
            )