from django.urls import path
from companies.views.companies import (
    CompanyAdminListView,
    CompanyAdminDetailView,
    CompanyOwnerDetailView,
)

urlpatterns = [
    # Rutas para administradores
    path('admin/companies/', CompanyAdminListView.as_view(), name='admin-company-list'),
    path('admin/companies/<int:pk>/', CompanyAdminDetailView.as_view(), name='admin-company-detail'),
    
    # Rutas para dueños de empresas
    path('owner/company/', CompanyOwnerDetailView.as_view(), name='owner-company-detail'),

]
