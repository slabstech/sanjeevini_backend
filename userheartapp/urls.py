from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserHeartAppViewSet

router = DefaultRouter()
router.register(r'', UserHeartAppViewSet)

urlpatterns = [
    # ... other URL patterns
    path('', include(router.urls)),
]