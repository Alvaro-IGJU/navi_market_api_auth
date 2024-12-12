from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet

router = DefaultRouter()
router.register(r'', CompanyViewSet, basename='company')  # Usar una base vacía

urlpatterns = router.urls
