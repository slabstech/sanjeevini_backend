from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.utils import extend_schema, extend_schema_serializer
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.openapi import OpenApiParameter

from .models import DoctorApp
from .serializers import DoctorAppSerializer

class DoctorAppPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class DoctorAppViewSet(viewsets.ModelViewSet):
    queryset = DoctorApp.objects.all().order_by('id')
    serializer_class = DoctorAppSerializer
    pagination_class = DoctorAppPagination

    @extend_schema(
        summary="List all doctor appointments",
        description="This endpoint retrieves a list of all doctor appointments. "
                    "You can filter the results by the doctor's name and paginate through the results.",
        responses={200: DoctorAppSerializer(many=True)},
        parameters=[
            OpenApiParameter(
                name='name',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Filter by doctor's name",
                required=False
            ),
            OpenApiParameter(
                name='page',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Page number",
                required=False
            ),
            OpenApiParameter(
                name='page_size',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Number of items per page",
                required=False
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve a single doctor appointment",
        description="This endpoint retrieves a single doctor appointment by its ID.",
        responses={200: DoctorAppSerializer},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)