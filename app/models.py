from django.db import models
from time import timezone
from django.contrib.auth.models import AbstractUser, BaseUserManager

class User(AbstractUser):
    mobile = models.CharField(max_length=100,default=0)

# Create your models here.
