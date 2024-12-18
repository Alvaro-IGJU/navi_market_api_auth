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
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from django.shortcuts import get_object_or_404
from openai import OpenAI

client = OpenAI(api_key="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")

from navi_market_api_auth.settings import OPENAI_API_KEY

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


class CompanyInteractionsView(APIView):
    """
    Devuelve las interacciones realizadas en los stands de una empresa específica,
    tanto el total como por cada stand.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, company_id):
        try:
            # Filtrar los stands por empresa
            stands = Stand.objects.filter(company_id=company_id)

            if not stands.exists():
                return Response(
                    {"error": "No se encontraron stands para esta empresa."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Obtener todas las interacciones relacionadas con estos stands
            interactions = Interaction.objects.filter(stand__in=stands)

            # Resumen general de interacciones por tipo
            interaction_summary = interactions.values("interaction_type").annotate(
                total_interactions=Count("id"),
                total_duration=Sum("interaction_duration")
            )

            # Datos específicos por stand
            stands_data = []
            for stand in stands:
                stand_interactions = interactions.filter(stand=stand).values("interaction_type").annotate(
                    total_interactions=Count("id"),
                    total_duration=Sum("interaction_duration")
                )
                stands_data.append({
                    "stand_id": stand.id,
                    "stand_name": stand.name,
                    "event_name": stand.event.name,  # Incluye el nombre del evento del stand
                    "total_interactions": sum([item["total_interactions"] for item in stand_interactions]),
                    "interaction_details": list(stand_interactions),
                })

            # Estructura de respuesta
            response_data = {
                "company_id": company_id,
                "total_interactions": interactions.count(),
                "interaction_details": list(interaction_summary),  # Resumen global
                "stands_details": stands_data,  # Interacciones por stand
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class CompanyEventVisitsSummaryView(APIView):
    """
    Devuelve el número de visitas de eventos donde la empresa tiene un stand,
    agrupadas por fecha.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, company_id):
        try:
            # Filtrar eventos donde la empresa tiene stands
            events_with_stands = Event.objects.filter(stands__company_id=company_id).distinct()

            if not events_with_stands.exists():
                return Response(
                    {"error": "No se encontraron eventos con stands de esta empresa."},
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
                "company_id": company_id,
                "events": list(events_data.values())
            }

            return Response(response_data, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)


class ChatbotView(APIView):
    """
    Chatbot para responder preguntas relacionadas con la empresa del stand.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, stand_id):
        try:
            # Log for debugging
            print(f"Recibida solicitud para el chatbot del stand {stand_id}")

            # Fetch stand and company information
            stand = Stand.objects.get(id=stand_id)
            company = stand.company
            question = request.data.get("question", "")
            print(f"Conectando con OpenAI para la empresa {company.name}")

            # OpenAI integration
            response = client.chat.completions.create(model="gpt-4o",
            messages=[
                {"role": "system", "content": f"Eres un asistente virtual de la empresa {company.name}."},
                {"role": "user", "content": question},
            ])
            chatbot_response = response.choices[0].message.content.strip()
            print(f"Respuesta del chatbot: {chatbot_response}")
            return Response({"response": chatbot_response}, status=200)

        except Stand.DoesNotExist:
            return Response({"error": "Stand no encontrado."}, status=404)

        except Exception as e:
            print(f"Error inesperado: {str(e)}")
            return Response({"error": str(e)}, status=500)