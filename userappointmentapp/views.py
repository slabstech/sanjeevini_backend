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

from .models import UserAppointmentApp
from .serializers import UserAppointmentAppSerializer

from rest_framework.pagination import PageNumberPagination

class UserAppointmentAppPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class UserAppointmentAppViewSet(viewsets.ModelViewSet):
    queryset = UserAppointmentApp.objects.all().order_by('id')
    serializer_class = UserAppointmentAppSerializer
    pagination_class = UserAppointmentAppPagination