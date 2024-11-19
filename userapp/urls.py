from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserAppViewSet

router = DefaultRouter()
router.register(r'', UserAppViewSet)

urlpatterns = [
    # ... other URL patterns
    path('', include(router.urls)),
]