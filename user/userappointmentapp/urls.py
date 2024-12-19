from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserAppointmentAppViewSet

router = DefaultRouter()
router.register(r'', UserAppointmentAppViewSet)

urlpatterns = [
    # ... other URL patterns
    path('', include(router.urls)),
]