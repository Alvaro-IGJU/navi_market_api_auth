from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager
from companies.models import Company

company_sectors = [
    "Tecnología e Informática",
    "Salud y Medicina",
    "Finanzas y Seguros",
    "Retail y Comercio",
    "Industria Automotriz",
    "Energía y Recursos Naturales",
    "Construcción e Infraestructura",
    "Telecomunicaciones",
    "Agricultura y Alimentación",
    "Transporte y Logística",
    "Medios y Entretenimiento",
    "Educación y Formación",
    "Inmobiliario",
    "Turismo y Hostelería",
    "Manufactura y Producción",
    "Química y Materiales",
    "Servicios Profesionales",
    "Otros",
]

companyPositions = [
  "CEO (Director General)",
  "COO (Director de Operaciones)",
  "CFO (Director Financiero)",
  "CTO (Director de Tecnología)",
  "CMO (Director de Marketing)",
  "CIO (Director de Sistemas de Información)",
  "Gerente de Recursos Humanos",
  "CSO (Chief Strategy Officer)",
  "CLO (Chief Legal Officer)",
  "Gerente de Operaciones",
  "Controller Financiero",
  "Director de Innovación",
  "Arquitecto de Software",
  "Desarrollador de Software",
  "Especialista en Ciberseguridad",
  "Analista de Datos (Data Analyst)",
  "Gerente de Marketing",
  "Especialista en SEO/SEM",
  "Gerente de Ventas",
  "Key Account Manager (KAM)",
  "Community Manager",
  "Project Manager",
  "Ingeniero de Procesos",
  "Gerente de Logística",
  "Consultor Estratégico",
  "Director Creativo",
  "Abogado Corporativo",
  "Asistente Ejecutivo",
  "Especialista en Atención al Cliente",
  "Business Development Manager (BDM)",
]


class Sector(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Nombre único del sector

    def __str__(self):
        return self.name


class Position(models.Model):
    title = models.CharField(max_length=255, unique=True)  # Título único de la posición

    def __str__(self):
        return self.title


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
