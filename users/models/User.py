
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from companies.models import Company
from .Position import Position
from .Sector import Sector
class User(AbstractUser):
    ROLE_CHOICES = (
        ('User', 'User'),
        ('Admin', 'Admin'),
        ('Company', 'Company'),
    )

    email = models.EmailField(unique=True)  # Campo email obligatorio y único
    username = models.CharField(max_length=150, unique=False)  # Campo username único
    company = models.CharField(max_length=255, blank=True, null=True)  # Campo existente (nombre de la empresa como texto)
    company_relation = models.ForeignKey(  # Nueva relación con el modelo Company
        Company, on_delete=models.SET_NULL, null=True, blank=True, related_name="users"
    )
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True, related_name="users")
    sector = models.ForeignKey(Sector, on_delete=models.SET_NULL, null=True, blank=True, related_name="users")
    profile_picture = models.TextField(blank=True, null=True)  # Campo para imagen en formato base64
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='User')  # Rol del usuario
    location = models.CharField(max_length=255, blank=True, null=True)  # Nuevo campo para la ubicación del usuario

    USERNAME_FIELD = 'email'  # Identificador principal
    REQUIRED_FIELDS = ['username']  # Campos requeridos además del email

    def __str__(self):
        return f"{self.email} - {self.get_role_display()}"
