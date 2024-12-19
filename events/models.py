# models.py
from django.db import models
from companies.models import Company

class Event(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True, null=True)
    image = models.TextField(blank=True, null=True)  # Cambia a TextField para almacenar base64
    max_stands = models.PositiveIntegerField(default=10)  # Número máximo de stands permitido


class Stand(models.Model):
    TYPE_CHOICES = [
        ('basic', 'Basic'),
        ('premium', 'Premium'),
        ('vip', 'VIP'),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="stands")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="stands")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    position = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='basic')
    pdf = models.TextField(blank=True, null=True)  # Almacenar PDF en formato base64


    def __str__(self):
        return self.name
