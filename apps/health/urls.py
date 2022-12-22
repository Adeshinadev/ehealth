# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, include
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('medical-records/', medical_records, name="medical-records"),
    path('book-appointment/', book_appointment, name="book-appointment"),
    path('search_medical_records/', search_medical_records, name="search_medical_records"),
    path("accept/<appointment_id>", accept, name="accept"),
    path("decline/<appointment_id>", decline, name="decline"),
    path("general_medical_report", general_medical_report, name="general_medical_report")

]
