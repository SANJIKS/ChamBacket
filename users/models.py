from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    surname = models.CharField(max_length=100, null=True, blank=True)
    points = models.PositiveIntegerField(default=0)