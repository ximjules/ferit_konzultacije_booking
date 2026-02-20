from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.db.models import Count
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic import DetailView, ListView

from .forms import BookingForm
from .models import AvailabilitySlot, Booking
from .utils import is_mentor, is_student


@login_required
def mentor_slots(request):
    if not is_mentor(request.user):
        return HttpResponseForbidden("Nemaš pristup ovoj stranici.")

    # dodamo info ima li booking
    slots = (
        AvailabilitySlot.objects.filter(mentor=request.user)
        .annotate(bookings_count=Count("bookings"))
        .order_by("start_at")
    )
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
            return redirect("booking:mentor_add_slot")

        try:
            start_dt = datetime.fromisoformat(start_at_raw)
            end_dt = datetime.fromisoformat(end_at_raw)
        except ValueError:
            messages.error(request, "Neispravan format datuma.")
            return redirect("booking:mentor_add_slot")

        if timezone.is_naive(start_dt):
            start_dt = timezone.make_aware(start_dt)
        if timezone.is_naive(end_dt):
            end_dt = timezone.make_aware(end_dt)

        if start_dt >= end_dt:
            messages.error(request, "Početak mora biti prije kraja termina.")
            return redirect("booking:mentor_add_slot")

        overlap = AvailabilitySlot.objects.filter(
            mentor=request.user,
            start_at__lt=end_dt,
            end_at__gt=start_dt,
        ).exists()
        if overlap:
            messages.error(request, "Termin se preklapa s postojećim terminom.")
            return redirect("booking:mentor_add_slot")

        AvailabilitySlot.objects.create(
            mentor=request.user,
            start_at=start_dt,
            end_at=end_dt,
        )
        messages.success(request, "Termin uspješno dodan.")
        return redirect("booking:mentor_slots")

    return render(request, "booking/mentor_add_slot.html")


class SlotListView(ListView):
    model = AvailabilitySlot
    template_name = "booking/slot_list.html"
    context_object_name = "slots"

    def get_queryset(self):
        # aktivni termini koji nisu završili i NEMAJU booking
        return (
            AvailabilitySlot.objects.filter(is_active=True, end_at__gt=timezone.now())
            .annotate(bookings_count=Count("bookings"))
            .filter(bookings_count=0)
            .select_related("mentor")
            .order_by("start_at")
        )


class SlotDetailView(DetailView):
    model = AvailabilitySlot
    template_name = "booking/slot_detail.html"
    context_object_name = "slot"


@login_required
def book_slot(request, slot_pk):
    slot = get_object_or_404(AvailabilitySlot, pk=slot_pk)

    if not is_student(request.user):
        return HttpResponseForbidden("Samo studenti mogu rezervirati termine.")

    # ako već postoji booking -> ne može se rezervirati
    if Booking.objects.filter(slot=slot).exists():
        messages.error(request, "Ovaj termin je već rezerviran.")
        return redirect("booking:home")

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = Booking(slot=slot, student=request.user)
            try:
                booking.full_clean()
                booking.save()
                messages.success(request, "Rezervacija uspješno napravljena.")
                return redirect("booking:my_bookings")
            except ValidationError as e:
                form.add_error(None, e)
    else:
        form = BookingForm()

    return render(request, "booking/booking_confirm.html", {"form": form, "slot": slot})


class MyBookingsView(LoginRequiredMixin, ListView):
    template_name = "booking/my_bookings.html"
    context_object_name = "bookings"

    def get_queryset(self):
        return (
            Booking.objects.filter(student=self.request.user)
            .select_related("slot", "slot__mentor")
            .order_by("-created_at")
        )


def home(request):
    slots = (
        AvailabilitySlot.objects.filter(is_active=True, end_at__gt=timezone.now())
        .annotate(bookings_count=Count("bookings"))
        .filter(bookings_count=0)
        .select_related("mentor")
        .order_by("start_at")
    )
    return render(request, "booking/home.html", {"slots": slots})
