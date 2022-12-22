# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, include
from .views import *


urlpatterns = [
    path('', login_view, name="login"),
    path('patient_login/', patient_login, name="patient_login"),
    path('health_worker_login/', health_worker_login, name="health_worker_login"),
    path('register/', register_user, name="register"),
    path("logout/", logout, name="logout"),
]
