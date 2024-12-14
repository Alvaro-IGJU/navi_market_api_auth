# models.py
from django.db import models
from companies.models import Company

class Event(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True, null=True)
    image = models.TextField(blank=True, null=True)  # Cambia a TextField para almacenar base64

class Stand(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="stands")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="stands")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    coordinates = models.JSONField(blank=True, null=True)
