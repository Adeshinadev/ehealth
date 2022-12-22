from django.contrib import admin

from apps.health.models import Medical_records, Appointment, Health_worker_stat

# Register your models here.
admin.site.register(Medical_records)
admin.site.register(Appointment)
admin.site.register(Health_worker_stat)
