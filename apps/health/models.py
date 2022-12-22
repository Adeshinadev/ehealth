from django.contrib.auth.models import User
from django.db import models

from apps.authentication.models import Profile


# Create your models here.
class Medical_records(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    age = models.CharField(max_length=10, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    medical_records = models.TextField()
    other_details = models.TextField()


class Appointment(models.Model):
    STATUS = (
        ("Pending", "Pending"),
        ("Declined", "Declined"),
        ("Accepted", "Accepted")
    )
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True, related_name="the_patient")
    address = models.TextField(max_length=500)
    state = models.TextField(max_length=500)
    date = models.DateTimeField()
    procedure = models.TextField()
    health_worker = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="doctor")
    status = models.CharField(max_length=100, choices=STATUS, null=True, blank=True)
    other = models.TextField()


class Health_worker_stat(models.Model):
    health_worker = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True,
                                      related_name="health_worker_stat")
    month = models.CharField(max_length=100, null=True, blank=True)
    year = models.CharField(max_length=100,null=True, blank=True)
    accepted = models.IntegerField(default=0)
    declined = models.IntegerField(default=0)
