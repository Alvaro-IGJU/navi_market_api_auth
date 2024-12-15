from django.db import models
from users.models import User
from events.models import Event, Stand

class Visit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="visits")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="visits")
    time_spent_seconds = models.IntegerField(default=0)  # Inicializamos con 0
    is_recurrent = models.BooleanField(default=False)
    visit_date = models.DateTimeField(auto_now_add=True)


class Interaction(models.Model):
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE, related_name="interactions")
    stand = models.ForeignKey(Stand, on_delete=models.CASCADE, related_name="interactions")
    interaction_type = models.CharField(max_length=50)  # e.g., "mailbox", "info_pc", etc.
    interaction_date = models.DateTimeField(auto_now_add=True)
    interaction_details = models.TextField(blank=True, null=True)
    interaction_duration = models.IntegerField(default=0)  # Duration in seconds

class Lead(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="leads")
    stand = models.ForeignKey(Stand, on_delete=models.CASCADE, related_name="leads")
    interest_score = models.IntegerField()
    funnel_stage = models.CharField(max_length=50)  # "cold", "warm", "hot"
