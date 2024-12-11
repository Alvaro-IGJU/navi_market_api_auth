from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager

class User(AbstractUser):
    email = models.EmailField(unique=True)  # Campo email obligatorio y único
    username = models.CharField(max_length=150, unique=True)  # Campo username único
    company = models.CharField(max_length=255, blank=True, null=True)  # Empresa del usuario
    position = models.CharField(max_length=255, blank=True, null=True)  # Cargo del usuario
    company_sector = models.CharField(max_length=255, blank=True, null=True)  # Sector de la empresa

    USERNAME_FIELD = 'email'  # Identificador principal
    REQUIRED_FIELDS = ['username']  # Campos requeridos además del email

    objects = CustomUserManager()

    def __str__(self):
        return self.email
