from django.urls import path
from .views import *

urlpatterns = [
    path('visits/register/<int:event_id>/', RegisterVisitView.as_view(), name='register-visit'),
    path('visits/close/<int:event_id>/', CloseVisitView.as_view(), name='close-visit'),
    path("register/<int:stand_id>/", RegisterInteractionView.as_view(), name="register-interaction"),
    path("update-duration/<int:interaction_id>/", UpdateInteractionDurationView.as_view(), name="update-interaction-duration"),
    path("companies/<int:company_id>/interactions/", CompanyInteractionsView.as_view(), name="company-interactions"),
    path("companies/<int:company_id>/events-visits/", CompanyEventVisitsSummaryView.as_view(), name="company-events-visits"),

]