from django.shortcuts import render
from .models import UserApp
from rest_framework import viewsets
from .models import UserApp
from .serializers import UserAppSerializer

from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import django_filters
from rest_framework import viewsets
from rest_framework.decorators import action

from datetime import datetime, timedelta
from rest_framework.response import Response
import requests

from django.utils import timezone
from datetime import timedelta
from rest_framework.pagination import LimitOffsetPagination


class UserAppViewSet(viewsets.ModelViewSet):
    queryset = UserApp.objects.all()
    serializer_class = UserAppSerializer

