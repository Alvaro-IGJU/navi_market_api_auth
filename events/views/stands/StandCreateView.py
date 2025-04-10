from rest_framework.views import APIView
from users.permissions import IsSuperUser
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from events.models import Event, Stand
from rest_framework.response import Response
from events.serializers import EventSerializer, StandSerializer
from PyPDF2 import PdfReader
from io import BytesIO
import base64

import re

YOUTUBE_VIDEO_ID_REGEX = r"^(?:https?:\/\/)?(?:www\.)?(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=))(?P<id>[0-9A-Za-z_-]{11}).*"


class StandCreateView(APIView):
    """
    Vista para crear un nuevo stand (Solo administradores).
    """
    permission_classes = [IsSuperUser]

    def post(self, request):
        try:
            # Obtener el evento
            event = Event.objects.get(pk=request.data["event"])

            # Validar si el evento alcanzó el número máximo de stands
            current_stand_count = Stand.objects.filter(event=event).count()
            if current_stand_count >= event.max_stands:
                return Response(
                    {"error": f"El evento '{event.name}' ya alcanzó el máximo de stands permitidos ({event.max_stands})."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Validar si ya existe un stand en la misma posición
            stands = Stand.objects.filter(event=event)
            for stand in stands:
                if int(stand.position) == int(request.data["position"]):
                    return Response(
                        {"error": "Ya existe un stand en esa posición."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            # Extraer la ID del video si `video_url` está presente
            video_url = request.data.get("url_video")
            print("VIDEO",video_url)
            if video_url:
                match = re.search(YOUTUBE_VIDEO_ID_REGEX, video_url)
                print("MATCH",match)

                if match:
                    request.data["url_video"] = match.group("id")  # Cambia a usar el grupo nombrado "id"
                else:
                    return Response(
                        {"error": "URL de video no válida."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            # Procesar el PDF si `prompts_pdf` está presente
            prompts_text = ""
            prompts_pdf = request.data.get("prompts_pdf")
            if prompts_pdf:
                try:
                    # Decodificar el PDF desde Base64
                    pdf_bytes = base64.b64decode(prompts_pdf)
                    pdf_stream = BytesIO(pdf_bytes)

                    # Leer el texto del PDF
                    reader = PdfReader(pdf_stream)
                    for page in reader.pages:
                        prompts_text += page.extract_text() + "\n"  # Concatenar el texto de las páginas
                except Exception as e:
                    return Response(
                        {"error": "Error al procesar el PDF", "details": str(e)},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            # Crear el stand
            stand_data = {
                **request.data,
                "prompts": prompts_text.strip(),  # Guardar los prompts extraídos
            }
            serializer = StandSerializer(data=stand_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Event.DoesNotExist:
            return Response(
                {"error": "El evento no existe."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": f"Error al crear el stand: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
