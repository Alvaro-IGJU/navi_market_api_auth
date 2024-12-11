from django.db import models
from companies.models import Company

class Event(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    virtual_location = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

class Stand(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="stands")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="stands")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    coordinates = models.JSONField(blank=True, null=True)
