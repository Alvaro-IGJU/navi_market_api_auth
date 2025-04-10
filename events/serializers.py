from rest_framework import serializers
from .models import Event, Stand

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'name', 'start_date', 'end_date', 'description', 'image', 'max_stands']

class StandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stand
        fields = '__all__'
        extra_kwargs = {
            'prompts': {'write_only': True},  # El campo "prompts" será solo para escritura
        }
