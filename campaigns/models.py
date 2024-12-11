from django.db import models
from events.models import Event, Stand

class Campaign(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="campaigns")
    stand = models.ForeignKey(Stand, on_delete=models.CASCADE, related_name="campaigns", null=True, blank=True)
    name = models.CharField(max_length=255)
    sent_date = models.DateTimeField(auto_now_add=True)
    open_rate = models.FloatField(default=0.0)  # Percentage of email opens (0-100)
