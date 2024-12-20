from rest_framework.views import APIView
from users.permissions import  IsSuperUser
from rest_framework import status
from rest_framework.response import Response
from events.serializers import EventSerializer


class EventCreateView(APIView):
    """
    Vista para crear un nuevo evento (Solo administradores).
    """
    permission_classes = [IsSuperUser]

    def post(self, request):
        print(request.data)
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

