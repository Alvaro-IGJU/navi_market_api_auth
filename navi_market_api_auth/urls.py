from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Endpoint para obtener tokens
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Endpoint para renovar tokens
    
    path('api/users/', include('users.urls')),
        # Rutas de las aplicaciones
    path('api/companies/', include('companies.urls')),   # Rutas de empresas
    path('api/events/', include('events.urls')),         # Rutas de eventos y stands
    path('api/interactions/', include('interactions.urls')), # Rutas de visitas e interacciones
    path('api/gamification/', include('gamification.urls')), # Rutas de gamificación
    path('api/campaigns/', include('campaigns.urls')),    # Rutas de campañas

]
