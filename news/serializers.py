# news/serializers.py
from rest_framework import serializers
from .models import Article
from myapp.models import HISTORY
class HistorySerializer(serializers.ModelSerializer):
  id = serializers.CharField(source='USER_PHONE')
  class Meta:
    model = HISTORY
    fields = ('id', 'APP_ID', 'DATE','POINT','DETAIL')