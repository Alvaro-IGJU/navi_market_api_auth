from rest_framework.routers import DefaultRouter
from .views import GamificationActivityViewSet

router = DefaultRouter()
router.register(r'gamification', GamificationActivityViewSet)

urlpatterns = router.urls
