from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from drf_spectacular import openapi

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/v1/userapp/', include('user.userapp.urls')),
    path('api/v1/doctorapp/', include('doctor.doctorapp.urls')),
    path('api/v1/inference/', include('inference.urls')),
    path('api/v1/doctorappointmentapp/', include('doctor.doctorappointmentapp.urls')),
    path('api/v1/prescriptionapp/', include('user.prescriptionapp.urls')),
    path('api/v1/userappointmentapp/', include('user.userappointmentapp.urls')),
    path('api/v1/userdiabetesapp/', include('user.userdiabetesapp.urls')),
    path('api/v1/userheartapp/', include('user.userheartapp.urls')),
    path('api/v1/userweightapp/', include('user.userweightapp.urls')),
]