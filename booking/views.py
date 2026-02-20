from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.db import transaction

from .models import AvailabilitySlot, Booking
from accounts.views import is_mentor
from datetime import datetime


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
        start_at_raw = request.POST.get("start_at")
        end_at_raw = request.POST.get("end_at")

        if not start_at_raw or not end_at_raw:
            messages.error(request, "Molim unesi početak i kraj termina.")
            return redirect("mentor_add_slot")

        # očekujemo format "YYYY-MM-DDTHH:MM" iz <input type="datetime-local">
        try:
            start_dt = datetime.fromisoformat(start_at_raw)
            end_dt = datetime.fromisoformat(end_at_raw)
        except ValueError:
            messages.error(request, "Neispravan format datuma.")
            return redirect("mentor_add_slot")

        # učini aware datetime ako je naive
        if timezone.is_naive(start_dt):
            start_dt = timezone.make_aware(start_dt)
        if timezone.is_naive(end_dt):
            end_dt = timezone.make_aware(end_dt)

        if start_dt >= end_dt:
            messages.error(request, "Početak mora biti prije kraja termina.")
            return redirect("mentor_add_slot")

        # provjeri preklapanje s već postojećim terminima mentora
        overlap = AvailabilitySlot.objects.filter(
            mentor=request.user,
            start_at__lt=end_dt,
            end_at__gt=start_dt,
        ).exists()
        if overlap:
            messages.error(request, "Termin se preklapa s postojećim terminom.")
            return redirect("mentor_add_slot")

        slot = AvailabilitySlot.objects.create(
            mentor=request.user,
            start_at=start_dt,
            end_at=end_dt,
        )
        messages.success(request, "Termin uspješno dodan.")
        return redirect("mentor_slots")

    return render(request, "booking/mentor_add_slot.html")


@login_required
def available_slots(request):
    """
    Lista svih slobodnih (ne-bookiranih) termina u budućnosti.
    """
    slots = AvailabilitySlot.objects.filter(
        start_at__gt=timezone.now()
    ).exclude(
        bookings__status='booked'
    ).order_by("start_at")
    return render(request, "booking/available_slots.html", {"slots": slots})


@login_required
def book_slot(request, slot_id):
    """
    Student rezervira termin. Ako je već bookiran, vraćamo poruku.
    """
    try:
        with transaction.atomic():
            # koristimo select_for_update kako bismo "zaključali" redak termina u DB dok provjeravamo/stvaramo rezervaciju
            slot = AvailabilitySlot.objects.select_for_update().get(pk=slot_id)

            # samo budući termini
            if slot.start_at <= timezone.now():
                messages.error(request, "Ne možeš rezervirati prošli ili tekući termin.")
                return redirect("available_slots")

            # provjeri postoji li aktivna rezervacija (booked) - ponovno pod lockom
            if slot.bookings.filter(status='booked').exists():
                messages.error(request, "Ovaj termin je već rezerviran.")
                return redirect("available_slots")

            # kreiraj rezervaciju
            Booking.objects.create(slot=slot, student=request.user, status='booked')
            messages.success(request, "Termin uspješno rezerviran.")
            return redirect("available_slots")
    except AvailabilitySlot.DoesNotExist:
        return redirect("available_slots")


def home(request):
    return render(request, "booking/home.html")
