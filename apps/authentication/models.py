# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="the_user")
    phone_number = models.CharField(max_length=100, unique=True)
    health_worker = models.BooleanField(default=False)
    patient = models.BooleanField(default=False)


