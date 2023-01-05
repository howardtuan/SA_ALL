from django.db import models
from django.utils import timezone

# Create your models here.
class client(models.Model):
    NAME = models.CharField(max_length=10)
    PHONE_NUMBER = models.CharField(max_length=20)
    PASSWORD = models.CharField(max_length=20)
    POINT = models.IntegerField()
    PHOTO = models.FileField()
    def add_points(self, points):
        self.POINT += points
        self.save()

class APP_LINK(models.Model):
    USER_PHONE = models.CharField(max_length=20)
    APP_ID = models.CharField(max_length=10)
    APP_USER_ID = models.CharField(max_length=10)

class EXCHANGE(models.Model):
    ID = models.AutoField(primary_key = True)
    USER_PHONE = models.CharField(max_length=10)
    DATE = models.DateTimeField()
    COST = models.IntegerField()
    ITEM_ID = models.IntegerField()
    ITEM_NAME = models.CharField(max_length=20)
    USED = models.BooleanField()

class HISTORY(models.Model):
    USER_PHONE = models.CharField(max_length=20)
    APP_ID = models.CharField(max_length=10)
    DATE = models.DateTimeField()
    POINT = models.IntegerField()
    DETAIL = models.CharField(max_length = 50)

class EXCHANGE_ITEM(models.Model):
    ID =  models.AutoField(primary_key = True)
    NAME = models.CharField(max_length=20)
    COST = models.IntegerField()
class DRIVE(models.Model):
    USER_PHONE = models.CharField(max_length=20)
    NAME = models.CharField(max_length=20)
    TIME = models.DateTimeField()
    USING = models.BooleanField()