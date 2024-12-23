from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from events.models import Stand
from openai import OpenAI

client = OpenAI(api_key="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")

from navi_market_api_auth.settings import OPENAI_API_KEY

class InteractionChatbotView(APIView):
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
                {"role": "system", "content": f"Eres un asistente virtual de la empresa {company.name}. Seguiras las siguientes instrucciones: {stand.prompts}. Contesta concisamente y no generes mucho texto, tiene que ser algo agradable pero rápido."},
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