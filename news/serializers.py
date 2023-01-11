# news/serializers.py

from rest_framework import serializers
from .models import Article
from myapp.models import HISTORY,client

class HistorySerializer(serializers.ModelSerializer):
  # id = serializers.CharField(source='USER_PHONE')
  class Meta:
    model = HISTORY
    fields = ('USER_PHONE', 'APP_ID', 'DATE','POINT','DETAIL','TANPI')
    
  def create(self, validated_data):
    client_id = validated_data.get('USER_PHONE')
    points = validated_data.get('POINT')
    tanpis = validated_data.get('TANPI')
    # count = client.objects.filter(USER_PHONE = client_id).count()
  
    member = client.objects.get(PHONE_NUMBER = client_id)
    member.add_points(points,tanpis)

    return super().create(validated_data)
