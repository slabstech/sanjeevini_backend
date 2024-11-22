from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserDiabetesAppViewSet

router = DefaultRouter()
router.register(r'', UserDiabetesAppViewSet)

urlpatterns = [
    # ... other URL patterns
    path('', include(router.urls)),
]