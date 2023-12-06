from django.db import models

class Backet(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    active_points = models.PositiveIntegerField(default=0)
    token = models.CharField(max_length=150, null=True, blank=True)