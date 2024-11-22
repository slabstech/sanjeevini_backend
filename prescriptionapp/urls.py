from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PrescriptionAppViewSet

router = DefaultRouter()
router.register(r'', PrescriptionAppViewSet)

urlpatterns = [
    # ... other URL patterns
    path('', include(router.urls)),
]