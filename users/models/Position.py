from django.db import models


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


class Position(models.Model):
    title = models.CharField(max_length=255, unique=True)  # Título único de la posición

    def __str__(self):
        return self.title