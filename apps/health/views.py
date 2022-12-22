from cProfile import Profile

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from .models import *
from .send_email import send_mail

conditions = ["Asthma", "Cancer", "Cardiac Disease", "Hypertension", "Malaria", "Chest Pain"]

months = ["Unknown",
          "January",
          "Febuary",
          "March",
          "April",
          "May",
          "June",
          "July",
          "August",
          "September",
          "October",
          "November",
          "December"]

now = datetime.now()

month = months[now.month]


# Create your views here.
@login_required(login_url="/login/")
def medical_records(request):
    profile = Profile.objects.get(user=request.user)

    text_of_medical_cond = ""
    if request.method == "POST":
        Medical_records.objects.filter(user=request.user).delete()
        create_record = Medical_records(user=request.user, other_details=request.POST['others'],
                                        age=request.POST["age"])
        create_record.save()
        get_record = Medical_records.objects.filter(user=request.user)
        for i in request.POST:
            if i in conditions:
                text_of_medical_cond = text_of_medical_cond + f",{request.POST[i]}"

        get_record.update(medical_records=text_of_medical_cond)
        return redirect("medical-records")

    else:
        if profile.patient:
            get_record = Medical_records.objects.filter(user=request.user)
            if get_record:
                return render(request, "patient/medical_record_form.html",
                              {"conditions": conditions, "medical_record": get_record.first()})

            return render(request, "patient/medical_record_form.html", {"conditions": conditions})
        else:
            records = Medical_records.objects.all()
            return render(request, "health_worker/medical_records.html", {"records": records, "conditions": conditions})


@login_required(login_url="/login/")
def search_medical_records(request):
    profile = Profile.objects.get(user=request.user)
    if profile.health_worker:
        condition = request.POST["condition"]
        records = Medical_records.objects.filter(medical_records__icontains=condition)
        return render(request, "health_worker/medical_records.html",
                      {"records": records, "conditions": conditions, "condition": condition, "change": True})
    else:
        return redirect("login")


@login_required(login_url="/login/")
def book_appointment(request):
    if request.method == "POST":
        address = request.POST["address"]
        state = request.POST["state"]
        date_str = request.POST["date"].replace("T", " ")
        procedure = request.POST["procedure"]
        other = request.POST["others"]

        doctor_id = int(request.POST["doctor_id"])
        doctor = Profile.objects.filter(id=doctor_id).first()
        user_profile = Profile.objects.filter(user=request.user).first()
        date = datetime.strptime(date_str.replace("-", "/"), "%Y/%m/%d %H:%M")
        if date < datetime.today() + timedelta(hours=24):
            messages.error(request, "Invalid appointment date, please enter a date at least 24 hours in the future")
            return redirect("patient_login")

        save_appt = Appointment(address=address, state=state, date=date, status="Pending", procedure=procedure,
                                health_worker=doctor,
                                other=other, user=user_profile)
        save_appt.save()
        messages.info(request,
                      f"You have booked an appointment with Dr. {doctor.user.first_name} {doctor.user.last_name} and "
                      f"you would be notified once confirmed")
        send_mail(f"{doctor.user.email}",
                  f"Hi Dr. {doctor.user.first_name}, {user_profile.user.first_name} {user_profile.user.last_name} "
                  f"has requested to book an appointment with you on {date_str}, "
                  f"please login to your dashboard to take action on the request.")
        return redirect("patient_login")


    else:
        return redirect("patient_login")


@login_required(login_url="/login/")
def accept(request, appointment_id):
    profile = Profile.objects.get(user=request.user)
    appt_obj = Appointment.objects.filter(id=appointment_id)
    if appt_obj.first().health_worker == profile:
        appt_obj.update(status="Accepted")
        stat = Health_worker_stat.objects.filter(month=month, year=now.year)
        if stat:
            stat.first().accepted = stat.first().accepted + 1
            stat.first().save()
        else:
            save_stat = Health_worker_stat(health_worker=profile, month=month, year=now.year, accepted=1)
            save_stat.save()

        messages.info(request, f"Appointment accepted for {appt_obj.first().user.user.first_name} "
                               f"{appt_obj.first().user.user.last_name}, on {appt_obj.first().date}")
        return redirect("health_worker_login")

    else:
        messages.error(request, "You are not permitted to perform this action")
        return redirect("health_worker_login")


@login_required(login_url="/login/")
def decline(request, appointment_id):
    profile = Profile.objects.get(user=request.user)
    appt_obj = Appointment.objects.filter(id=appointment_id)
    if appt_obj.first().health_worker == profile:
        appt_obj.update(status="Declined")
        stat = Health_worker_stat.objects.filter(month=month, year=now.year)
        if stat:
            stat.first().declined = stat.first().declined + 1
            stat.first().save()
        else:
            save_stat = Health_worker_stat(health_worker=profile, month=month, year=now.year, declined=1)
            save_stat.save()
        messages.info(request, f"Appointment Declined")
        return redirect("health_worker_login")

    else:
        messages.error(request, "You are not permitted to perform this action")
        return redirect("health_worker_login")


@login_required(login_url="/login/")
def general_medical_report(request):
    stats = []
    for i in conditions:
        stat = []
        cond = Medical_records.objects.filter(medical_records__icontains=i).count()
        print(cond)
        stat.append(i)
        stat.append(cond)
        stats.append(stat)
    print(stats,'kddk')

    return render(request, "home/general_report.html",
                  {"stats":stats})
