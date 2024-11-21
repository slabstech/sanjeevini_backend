from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DoctorAppointmentAppViewSet

router = DefaultRouter()
router.register(r'', DoctorAppointmentAppViewSet)

urlpatterns = [
    # ... other URL patterns
    path('', include(router.urls)),
]