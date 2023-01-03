# news/views.py
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Article
from .serializers import HistorySerializer
from myapp.models import HISTORY

class HISTORYViewSet(viewsets.ModelViewSet):
  queryset = HISTORY.objects.all()
  serializer_class = HistorySerializer
  permission_classes = (AllowAny,)