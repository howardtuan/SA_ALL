# news/serializers.py
from rest_framework import serializers
from .models import Article
from myapp.models import HISTORY
class HistorySerializer(serializers.ModelSerializer):
  class Meta:
    model = HISTORY
    fields = '__all__'