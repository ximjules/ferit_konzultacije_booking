from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.db import transaction
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.core.exceptions import ValidationError

from .models import AvailabilitySlot, Booking
from .utils import is_mentor
from datetime import datetime
from .forms import BookingForm


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


class SlotListView(ListView):
    model = AvailabilitySlot
    template_name = "booking/slot_list.html"
    context_object_name = "slots"

    def get_queryset(self):
        # Prikaži samo aktivne termine koji još nisu završili
        return AvailabilitySlot.objects.filter(is_active=True, end_at__gt=timezone.now()).order_by("start_at")


class SlotDetailView(DetailView):
    model = AvailabilitySlot
    template_name = "booking/slot_detail.html"
    context_object_name = "slot"


@login_required
def book_slot(request, slot_pk):
    slot = get_object_or_404(AvailabilitySlot, pk=slot_pk)
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = Booking(slot=slot, student=request.user)
            try:
                booking.full_clean()
                booking.save()
                messages.success(request, "Rezervacija uspješno napravljena.")
                return redirect(reverse("booking:my_bookings"))
            except ValidationError as e:
                form.add_error(None, e)
    else:
        form = BookingForm()
    return render(request, "booking/booking_confirm.html", {"form": form, "slot": slot})


class MyBookingsView(LoginRequiredMixin, ListView):
    template_name = "booking/my_bookings.html"
    context_object_name = "bookings"

    def get_queryset(self):
        return Booking.objects.filter(student=self.request.user).order_by("-created_at")


def home(request):
    return render(request, "booking/home.html")
