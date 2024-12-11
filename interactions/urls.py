from rest_framework.routers import DefaultRouter
from .views import VisitViewSet, InteractionViewSet, LeadViewSet

router = DefaultRouter()
router.register(r'visits', VisitViewSet)
router.register(r'interactions', InteractionViewSet)
router.register(r'leads', LeadViewSet)

urlpatterns = router.urls
