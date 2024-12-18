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

from .models import UserDiabetesApp
from .serializers import UserDiabetesAppSerializer

from rest_framework.pagination import PageNumberPagination

class UserDiabetesAppPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class UserDiabetesAppViewSet(viewsets.ModelViewSet):
    queryset = UserDiabetesApp.objects.all().order_by('id')
    serializer_class = UserDiabetesAppSerializer
    pagination_class = UserDiabetesAppPagination