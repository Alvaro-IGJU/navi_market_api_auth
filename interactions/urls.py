from django.urls import path
from .views import *
from interactions.views.visits import (
    VisitRegisterView,
    VisitCloseView,
    VisitCompanyEventSummaryView,
    VisitAdminEventSummaryView  # Asegúrate de importar tu nueva vista
)
from interactions.views.interactions import (
    InteractionRegisterView,
    InteractionChatbotView,
    InteractionUpdateDurationView, 
    InteractionCompaniesView
)

urlpatterns = [
    # Rutas para visitas
    path('visits/register/<int:event_id>/', VisitRegisterView.as_view(), name='register-visit'),
    path('visits/close/<int:event_id>/', VisitCloseView.as_view(), name='close-visit'),
    
    # Rutas para interacciones
    path("register/<int:stand_id>/", InteractionRegisterView.as_view(), name="register-interaction"),
    path("chatbot/<int:stand_id>/", InteractionChatbotView.as_view(), name="chatbot-interaction"),
    path("update-duration/<int:interaction_id>/", InteractionUpdateDurationView.as_view(), name="update-interaction-duration"),
    path("companies/<int:company_id>/interactions/", InteractionCompaniesView.as_view(), name="company-interactions"),
    path("companies/<int:company_id>/events-visits/", VisitCompanyEventSummaryView.as_view(), name="company-events-visits"),
    
    # Nueva URL para el resumen de visitas para el admin
    path("admin/events-visits-summary/", VisitAdminEventSummaryView.as_view(), name="admin-events-visits-summary"),  # Nueva ruta para admin
]
