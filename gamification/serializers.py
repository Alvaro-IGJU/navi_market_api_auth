from rest_framework import serializers
from .models import GamificationActivity

class GamificationActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = GamificationActivity
        fields = '__all__'
