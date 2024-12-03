
from django.contrib import admin
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, include

schema_view = get_schema_view(
    openapi.Info(
        title="Sanjeevini",
        default_version='v1',
        description="AI Health App",
        terms_of_service="https://www.sanjeevini.me/",
        contact=openapi.Contact(email="info@slabstech.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    urlconf='sanjeevini.urls',
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/v1/userapp/', include('userapp.urls')),
    path('api/v1/doctorapp/', include('doctorapp.urls')),
    path('api/v1/inference/', include('inference.urls')),
    path('api/v1/doctorappointmentapp/', include('doctorappointmentapp.urls')),
    path('api/v1/prescriptionapp/', include('prescriptionapp.urls')),
    path('api/v1/userappointmentapp/', include('userappointmentapp.urls')),
    path('api/v1/userdiabetesapp/', include('userdiabetesapp.urls')),
    path('api/v1/userheartapp/', include('userheartapp.urls')),
    path('api/v1/usermaternityapp/', include('usermaternityapp.urls')),
    path('api/v1/userweightapp/', include('userweightapp.urls')),
]
