# news/views.py
from rest_framework import generics
from requests import Response
from rest_framework.views import APIView
from rest_framework import status

from rest_framework import viewsets,generics
from rest_framework.permissions import AllowAny
from .models import Article
from .serializers import HistorySerializer
from myapp.models import HISTORY,client

class HISTORYViewSet(viewsets.ModelViewSet):
  queryset = HISTORY.objects.all()
  serializer_class = HistorySerializer
  permission_classes = (AllowAny,)


