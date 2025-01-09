from django.db import models
from users.models import User
from events.models import Event, Stand
from django.core.exceptions import ValidationError

class Visit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="visits")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="visits")
    time_spent_seconds = models.IntegerField(default=0)  # Inicializamos con 0
    is_recurrent = models.BooleanField(default=False)
    visit_date = models.DateTimeField(auto_now_add=True)

class Interaction(models.Model):
    # Opciones predefinidas para interaction_type
    INTERACTION_TYPE_CHOICES = [
        ('mailbox', 'Mailbox'),
        ('info_pc', 'Info PC'),
        ('play_video', 'Play Video'),
        ('download_catalog', 'Download Catalog'),
        ('schedule_meeting', 'Schedule Meeting'),
        ('talk_chatbot', 'Talk Chatbot'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    visit = models.ForeignKey(Visit, on_delete=models.CASCADE, related_name="interactions")
    stand = models.ForeignKey(Stand, on_delete=models.CASCADE, related_name="interactions")
    interaction_type = models.CharField(
        max_length=50,
        choices=INTERACTION_TYPE_CHOICES,  # Limitar a las opciones predefinidas
    )
    interaction_date = models.DateTimeField(auto_now_add=True)
    interaction_duration = models.DecimalField(
        max_digits=10,  # Tamaño máximo (e.g., 9999999.99)
        decimal_places=2,  # Mantener solo 2 decimales
        default=0.00
    )
    # Campo opcional de estado para schedule_meeting
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        blank=True,  # Permitimos que no esté definido para otros tipos
        null=True
    )

    def clean(self):
        """
        Validar que el campo 'status' solo se use con el tipo 'schedule_meeting'.
        """
        if self.status and self.interaction_type != 'schedule_meeting':
            raise ValidationError("El campo 'status' solo es válido para 'schedule_meeting'.")

    def __str__(self):
        return f"{self.interaction_type} at {self.stand.name}"

class Lead(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="leads")
    stand = models.ForeignKey(Stand, on_delete=models.CASCADE, related_name="leads")
    interest_score = models.IntegerField()
    funnel_stage = models.CharField(max_length=50)  # "cold", "warm", "hot"
