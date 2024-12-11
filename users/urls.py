from django.urls import path, include
from .views import LoginView, RegisterView, ProfileView

urlpatterns = [
    # Rutas de autenticación y perfil
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),

    # Rutas de las aplicaciones
    path('companies/', include('companies.urls')),   # Rutas de empresas
    path('events/', include('events.urls')),         # Rutas de eventos y stands
    path('interactions/', include('interactions.urls')), # Rutas de visitas e interacciones
    path('gamification/', include('gamification.urls')), # Rutas de gamificación
    path('campaigns/', include('campaigns.urls')),    # Rutas de campañas
]
