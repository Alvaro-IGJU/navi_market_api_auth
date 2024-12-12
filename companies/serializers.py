from rest_framework import serializers
from .models import Company

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'sector', 'contact_email', 'contact_phone', 'website', 'description', 'created_at']
        read_only_fields = ['created_at']
