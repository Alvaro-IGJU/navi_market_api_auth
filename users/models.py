from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager

class User(AbstractUser):
    email = models.EmailField(unique=True)  # Campo email obligatorio y único
    username = models.CharField(max_length=150, unique=True)  # Campo username único

    USERNAME_FIELD = 'email'  # Identificador principal
    REQUIRED_FIELDS = ['username']  # Campos requeridos además del email

    objects = CustomUserManager()

    def __str__(self):
        return self.email
