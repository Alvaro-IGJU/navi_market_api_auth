from rest_framework.routers import DefaultRouter
from .views import EventViewSet, StandViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'stands', StandViewSet)

urlpatterns = router.urls
