from interactions.models import Visit
from events.models import Event
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsSuperUser
from rest_framework.views import APIView
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate

class VisitAdminEventSummaryView(APIView):
    """
    Devuelve el número de visitas de eventos donde las empresas tienen stands,
    agrupadas por fecha, para todas las compañías.
    """
    permission_classes = [IsAuthenticated, IsSuperUser]

    def get(self, request):
        try:
            # Filtrar eventos donde cualquier empresa tenga stands
            events_with_stands = Event.objects.filter(stands__company__isnull=False).distinct()

            if not events_with_stands.exists():
                return Response(
                    {"error": "No se encontraron eventos con stands."},
                    status=404
                )

            # Filtrar visitas únicamente para estos eventos
            visits = (
                Visit.objects.filter(event__in=events_with_stands)
                .values("event__id", "event__name")
                .annotate(
                    date=TruncDate("visit_date"),
                    total_visits=Count("id"),
                    total_time_spent=Sum("time_spent_seconds")
                )
                .order_by("event__id", "date")
            )

            # Estructurar datos agrupados por evento
            events_data = {}
            for visit in visits:
                event_id = visit["event__id"]
                if event_id not in events_data:
                    events_data[event_id] = {
                        "event_id": event_id,
                        "event_name": visit["event__name"],
                        "visits": [],
                    }
                events_data[event_id]["visits"].append({
                    "date": visit["date"].strftime("%Y-%m-%d"),
                    "total_visits": visit["total_visits"],
                    "total_time_spent": visit["total_time_spent"]
                })

            # Convertir a lista para la respuesta
            response_data = {
                "events": list(events_data.values())
            }

            return Response(response_data, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
