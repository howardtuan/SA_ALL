from django.db import models
from django.utils import timezone

# Create your models here.
class client(models.Model):
    NAME = models.CharField(max_length=10)
    PHONE_NUMBER = models.CharField(max_length=20)
    PASSWORD = models.CharField(max_length=20)
    POINT = models.IntegerField()

class APP_LINK(models.Model):
    USER_PHONE = models.CharField(max_length=20)
    APP_ID = models.CharField(max_length=10)
    APP_USER_ID = models.CharField(max_length=10)

class EXCHANGE(models.Model):
    USER_PHONE = models.CharField(max_length=10)
    DATE = models.DateField
    COST = models.IntegerField()
    ITEM_ID = models.IntegerField()

class HISTORY(models.Model):
    USER_PHONE = models.CharField(max_length=20)
    APP_ID = models.CharField(max_length=10)
    DATE = models.DateField
    POINT = models.IntegerField()
    DETAIL = models.CharField(max_length = 50)

class EXCHANGE_ITEM(models.Model):
    ID =  models.AutoField
    NAME = models.CharField(max_length=20)
    COST = models.IntegerField