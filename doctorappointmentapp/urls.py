from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DoctorAppViewSet

router = DefaultRouter()
router.register(r'', DoctorAppViewSet)

urlpatterns = [
    # ... other URL patterns
    path('', include(router.urls)),
]