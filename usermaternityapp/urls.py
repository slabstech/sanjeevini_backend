from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserMaternityAppViewSet

router = DefaultRouter()
router.register(r'', UserMaternityAppViewSet)

urlpatterns = [
    # ... other URL patterns
    path('', include(router.urls)),
]