from django.shortcuts import render

# Create your views here.
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.shortcuts import redirect, render


def register(request):
    # registracija samo za studente
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # dodaj usera u group "student" (ako postoji)
            student_group, _ = Group.objects.get_or_create(name="student")
            user.groups.add(student_group)

            login(request, user)
            messages.success(request, "Registracija uspješna. Dobrodošla!")
            return redirect("dashboard")
    else:
        form = UserCreationForm()

    return render(request, "accounts/register.html", {"form": form})


@login_required
def dashboard(request):
    # redirect ovisno o ulozi
    if request.user.is_superuser:
        return render(request, "accounts/dashboard_admin.html")

    if request.user.groups.filter(name="mentor").exists():
        return render(request, "accounts/dashboard_mentor.html")

    # default: student
    return render(request, "accounts/dashboard_student.html")
