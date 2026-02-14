from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.utils import timezone

from .models import AvailabilitySlot
from accounts.views import is_mentor


@login_required
def mentor_slots(request):
    if not is_mentor(request.user):
        return HttpResponseForbidden("Nemaš pristup ovoj stranici.")

    slots = AvailabilitySlot.objects.filter(mentor=request.user).order_by("start_at")
    return render(request, "booking/mentor_slots.html", {"slots": slots})


@login_required
def mentor_add_slot(request):
    if not is_mentor(request.user):
        return HttpResponseForbidden("Nemaš pristup ovoj stranici.")

    if request.method == "POST":
        start_at = request.POST.get("start_at")
        end_at = request.POST.get("end_at")

        if not start_at or not end_at:
            messages.error(request, "Molim unesi početak i kraj termina.")
            return redirect("mentor_add_slot")

        # Django prima datetime-local kao "YYYY-MM-DDTHH:MM" string
        # Spremamo ga direktno; za projekt je OK (kasnije možemo timezone finije)
        slot = AvailabilitySlot.objects.create(
            mentor=request.user,
            start_at=start_at,
            end_at=end_at,
        )
        messages.success(request, "Termin uspješno dodan.")
        return redirect("mentor_slots")

    return render(request, "booking/mentor_add_slot.html")



def home(request):
    return render(request, "booking/home.html")
