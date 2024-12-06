from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import django_filters
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from django.utils import timezone
from datetime import datetime, timedelta
import requests

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import DoctorApp
from .serializers import DoctorAppSerializer

from rest_framework.pagination import PageNumberPagination

class DoctorAppPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class DoctorAppViewSet(viewsets.ModelViewSet):
    queryset = DoctorApp.objects.all().order_by('id')
    serializer_class = DoctorAppSerializer
    pagination_class = DoctorAppPagination

    @swagger_auto_schema(
        operation_summary="List all doctor appointments",
        operation_description="This endpoint retrieves a list of all doctor appointments. "
                              "You can filter the results by the doctor's name and paginate through the results.",
        operation_id="listDoctorAppointments",
        tags=["DoctorApp"],
        responses={200: DoctorAppSerializer(many=True)},
        manual_parameters=[
            openapi.Parameter(
                name='name',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Filter by doctor's name",
                required=False
            ),
            openapi.Parameter(
                name='page',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Page number",
                required=False
            ),
            openapi.Parameter(
                name='page_size',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Number of items per page",
                required=False
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve a single doctor appointment",
        operation_description="This endpoint retrieves a single doctor appointment by its ID.",
        operation_id="retrieveDoctorAppointment",
        tags=["DoctorApp"],
        responses={200: DoctorAppSerializer},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)