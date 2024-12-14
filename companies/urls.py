from django.urls import path
from .views import (
    AdminCompanyListView,
    AdminCompanyDetailView,
    OwnerCompanyDetailView,
)

urlpatterns = [
    # Rutas para administradores
    path('admin/companies/', AdminCompanyListView.as_view(), name='admin-company-list'),
    path('admin/companies/<int:pk>/', AdminCompanyDetailView.as_view(), name='admin-company-detail'),
    
    # Rutas para dueños de empresas
    path('owner/company/', OwnerCompanyDetailView.as_view(), name='owner-company-detail'),
]
