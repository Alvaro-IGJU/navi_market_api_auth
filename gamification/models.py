from django.db import models
from users.models import User
from events.models import Event

class GamificationActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="gamification_activities")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="gamification_activities")
    activity_type = models.CharField(max_length=50)  # "challenge", "reward"
    activity_date = models.DateTimeField(auto_now_add=True)
    reward_value = models.IntegerField(default=0)  # Value of the reward (points, tokens, etc.)
