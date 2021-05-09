from django.db import models
from django.contrib.auth.models import User

class Group(models.Model):
    Owner = models.ForeignKey(User, on_delete=models.CASCADE)
    Groupname = models.TextField(blank=False)
    Brokers = models.TextField(blank=True)