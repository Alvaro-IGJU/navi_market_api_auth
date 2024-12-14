from django.urls import path
from .views import (
    EventListView, EventRetrieveView, EventCreateView,
    EventUpdateView, EventDeleteView, StandListView, StandCreateView, StandUpdateView, StandDeleteView
)

urlpatterns = [
    path('', EventListView.as_view(), name='event-list'),
    path('<int:pk>/', EventRetrieveView.as_view(), name='event-detail'),
    path('create/', EventCreateView.as_view(), name='event-create'),
    path('<int:pk>/update/', EventUpdateView.as_view(), name='event-update'),
    path('<int:pk>/delete/', EventDeleteView.as_view(), name='event-delete'),

    path('stands/', StandListView.as_view(), name='stand-list'),
    path('stands/create/', StandCreateView.as_view(), name='stand-create'),
    path('stands/<int:pk>/update/', StandUpdateView.as_view(), name='stand-update'),
    path('stands/<int:pk>/delete/', StandDeleteView.as_view(), name='stand-delete'),
]
