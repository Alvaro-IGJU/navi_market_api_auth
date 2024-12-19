from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from .models import Event, Stand
from rest_framework.response import Response
from .serializers import EventSerializer, StandSerializer
from PyPDF2 import PdfReader
from io import BytesIO
import base64

