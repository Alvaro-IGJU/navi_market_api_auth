from django.urls import path
from .views import *
from interactions.views.visits import (
    VisitRegisterView,
    VisitCloseView,
    VisitCompanyEventSummaryView,
    VisitAdminEventSummaryView  # Asegúrate de importar tu nueva vista
)
from interactions.views.interactions import *

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
    path('companies/<int:company_id>/users-location/', InteractionUsersLocationView.as_view(), name='users-location'),
    path('companies/<int:company_id>/user-positions/', InteractionCompanyUserPositionsView.as_view(), name='user-positions'),
    path('companies/<int:company_id>/user-sectors/', InteractionCompanyUserSectorsView.as_view(), name='user-sectors'),
    path('companies/<int:company_id>/interested-users/', GetCompanyInterestedUsers.as_view(), name='get_interested_users'),
    path('companies/<int:company_id>/interest-funnel/', GetInterestFunnelViewByCompany.as_view(), name='get_interested_users'),
    path('companies/<int:company_id>/scheduled-meeting/', UsersScheduledMeetingView.as_view(), name='users-scheduled-meeting'),


    # Nueva URL para el resumen de visitas para el admin
    path("admin/events-visits-summary/", VisitAdminEventSummaryView.as_view(), name="admin-events-visits-summary"),  # Nueva ruta para admin
]
