from django.urls import path
from events.views.events import (
    EventListView,
    EventRetrieveView,
    EventCreateView,
    EventUpdateView,
    EventDeleteView,
    EventStandsView,
)
from events.views.stands import (
    StandListView,
    StandCreateView,
    StandUpdateView,
    StandDeleteView,
    GetStandByIdView
    )


urlpatterns = [
    path('', EventListView.as_view(), name='event-list'),
    path('<int:pk>/', EventRetrieveView.as_view(), name='event-detail'),
    path('create/', EventCreateView.as_view(), name='event-create'),
    path('<int:pk>/update/', EventUpdateView.as_view(), name='event-update'),
    path('<int:pk>/delete/', EventDeleteView.as_view(), name='event-delete'),
    path('<int:event_id>/stands/', EventStandsView.as_view(), name='event-stands'),

    path('stands/', StandListView.as_view(), name='stand-list'),
    path("stands/<int:stand_id>/", GetStandByIdView.as_view(), name="get-stand-by-id"),
    path('stands/create/', StandCreateView.as_view(), name='stand-create'),
    path('stands/<int:pk>/update/', StandUpdateView.as_view(), name='stand-update'),
    path('stands/<int:pk>/delete/', StandDeleteView.as_view(), name='stand-delete'),
]
