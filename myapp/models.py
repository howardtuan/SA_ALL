from django.db import models
from django.utils import timezone

# Create your models here.
class client(models.Model):
    NAME=models.CharField(max_length=10)
    PHONE_NUMBER=models.CharField(max_length=20)
    PASSWORD=models.CharField(max_length=20)
    POINT=models.IntegerField()