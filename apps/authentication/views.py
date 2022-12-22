# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout as auth_logout
from .forms import LoginForm, SignUpForm
from django.contrib.auth.models import User

from .models import Profile
from apps.health.models import *


@login_required(login_url="/login/")
def patient_login(request):
    doctors = Profile.objects.filter(health_worker=True)
    user_profile = Profile.objects.get(user=request.user)
    appointments = Appointment.objects.filter(user=user_profile)
    pending_appointments = Appointment.objects.filter(user=user_profile, status="Pending").count()
    declined_appointments = Appointment.objects.filter(user=user_profile, status="Declined").count()
    return render(request, "patient/index.html",
                  {"doctors": doctors, "appointments": appointments, "appointment_count": len(appointments),
                   "declined_appointments": declined_appointments,
                   "pending_appointments": pending_appointments, "user_profile": user_profile})


@login_required(login_url="/login/")
def health_worker_login(request):
    user_profile = Profile.objects.get(user=request.user)
    appointments = Appointment.objects.filter(health_worker=user_profile).order_by("-id")
    accepted_appointments = Appointment.objects.filter(health_worker=user_profile, status="Accepted").count()
    pending_appointments = Appointment.objects.filter(health_worker=user_profile, status="Pending").count()
    declined_appointments = Appointment.objects.filter(health_worker=user_profile, status="Declined").count()
    stats_list = []
    stats_obj = Health_worker_stat.objects.filter(health_worker=user_profile)
    for i in stats_obj:
        stat_obj = [i.month, i.accepted, i.declined]
        stats_list.append(stat_obj)
    print(stats_list, "ksjj")
    return render(request, "patient/health_login.html",
                  {"appointments": appointments, "appointment_count": len(appointments),
                   "declined_appointments": declined_appointments, "pending_appointments": pending_appointments,
                   "accepted_appointments": accepted_appointments, "stats_list": stats_list,
                   "user_profile": user_profile})


def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username").lower()
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                profile = Profile.objects.get(user=request.user)
                if profile.patient:
                    return redirect("patient_login")
                else:
                    return redirect("health_worker_login")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    if request.method == "POST":
        email = request.POST["email"].strip().lower()
        phone_no = request.POST["phone_no"].strip()
        first_name = request.POST["first_name"].strip()
        last_name = request.POST["last_name"].strip()
        password = request.POST["password"]
        user_type = int(request.POST["user_type"])
        for i in request.POST:
            print(i)
        if user_type == 1:
            health_worker = False
            patient = True
        else:
            health_worker = True
            patient = False
        try:
            user = User.objects.create_user(username=email, email=email, password=password, first_name=first_name,
                                            last_name=last_name)
            profile = Profile.objects.filter(user=user)
            profile.update(phone_number=phone_no, health_worker=health_worker, patient=patient)
            messages.info(request, "Account created, proceed to login")
        except IntegrityError:
            User.objects.filter(username=email).delete()
            messages.error(request, "Email or phone number already taken")
            return redirect("register")

        return redirect("login")

    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form})


def logout(request):
    auth_logout(request)
    return redirect('login')
