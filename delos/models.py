from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.

class User(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=10)
    sex = models.CharField(max_length=2)
    age = models.IntegerField()
    coin = models.IntegerField()
    signin_date = models.DateTimeField(default=timezone.now)