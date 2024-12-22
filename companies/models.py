from django.db import models
from users.models import Sector

class Company(models.Model):
    name = models.CharField(max_length=255)
    sector = models.ForeignKey(Sector, on_delete=models.SET_NULL, null=True, blank=True, related_name="companies")  # Relación con Sector
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=50, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
