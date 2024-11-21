from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserWeightAppViewSet

router = DefaultRouter()
router.register(r'', UserWeightAppViewSet)

urlpatterns = [
    # ... other URL patterns
    path('', include(router.urls)),
]