# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
  email = models.EmailField(max_length=100)
  tel = models.CharField(max_length=50)
  sports = models.CharField(max_length=50)
  location = models.CharField(max_length = 50)
  location_code = models.CharField(max_length=50)
  x = models.CharField(max_length=50)
  y = models.CharField(max_length=50)

