from django.db import models

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

class Sector(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Nombre único del sector

    def __str__(self):
        return self.name