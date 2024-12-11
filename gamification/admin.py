from django.contrib import admin
from django.apps import apps

# Registra automáticamente todos los modelos de la app 'gamification'
app = apps.get_app_config('gamification')

for model_name, model in app.models.items():
    admin.site.register(model)
