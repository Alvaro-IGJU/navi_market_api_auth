from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *;

# Rutas con DefaultRouter para Position y Sector
router = DefaultRouter()
router.register(r'positions', PositionViewSet, basename='position')  # Rutas para posiciones
router.register(r'sectors', SectorViewSet, basename='sector')  # Rutas para sectores

router.register(r'admin/users', AdminUserViewSet, basename='admin-users')
router.register(r'admin/positions', AdminPositionViewSet, basename='admin-positions')
router.register(r'admin/sectors', AdminSectorViewSet, basename='admin-sectors')

urlpatterns = [
    # Rutas de autenticación y perfil
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    
    # Rutas generadas automáticamente por el DefaultRouter
    path('', include(router.urls)),  # Incluye las rutas de positions y sectors

    path('admin/create-company-user/', CreateCompanyUserView.as_view(), name='create_company_user'),

]
