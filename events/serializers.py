from rest_framework import serializers
from .models import Event, Stand

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class StandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stand
        fields = '__all__'
