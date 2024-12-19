from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views.positions import PositionViewSet;
from users.views.sectors import (
    SectorViewSet,
)
from users.views.users import (
    UserLoginView,
    UserRegisterView,
    UserProfileView,
    UserChangePasswordView,
    AdminUserViewSet,
    AdminPositionViewSet,
    AdminSectorViewSet,
    AdminCreateCompanyUserView
)
# Rutas con DefaultRouter para Position y Sector
router = DefaultRouter()
router.register(r'positions', PositionViewSet, basename='position')  # Rutas para posiciones
router.register(r'sectors', SectorViewSet, basename='sector')  # Rutas para sectores

router.register(r'admin/users', AdminUserViewSet, basename='admin-users')
router.register(r'admin/positions', AdminPositionViewSet, basename='admin-positions')
router.register(r'admin/sectors', AdminSectorViewSet, basename='admin-sectors')

urlpatterns = [
    # Rutas de autenticación y perfil
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('change-password/', UserChangePasswordView.as_view(), name='change_password'),
    
    # Rutas generadas automáticamente por el DefaultRouter
    path('', include(router.urls)),  # Incluye las rutas de positions y sectors

    path('admin/create-company-user/', AdminCreateCompanyUserView.as_view(), name='create_company_user'),

]
# dK0fjASlM8G3