from django.contrib import admin
from .models import AvailabilitySlot, Booking


@admin.register(AvailabilitySlot)
class AvailabilitySlotAdmin(admin.ModelAdmin):
    list_display = ("mentor", "start_at", "end_at", "is_active")
    list_filter = ("mentor", "is_active")
    search_fields = ("mentor__username",)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("student", "slot", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("student__username", "slot__mentor__username")
