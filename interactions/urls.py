from django.urls import path
from .views import RegisterVisitView, CloseVisitView

urlpatterns = [
    path('visits/register/<int:event_id>/', RegisterVisitView.as_view(), name='register-visit'),
    path('visits/close/<int:event_id>/', CloseVisitView.as_view(), name='close-visit'),
]