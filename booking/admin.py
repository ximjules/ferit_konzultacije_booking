from django.contrib import admin
from .models import AvailabilitySlot, Booking

@admin.register(AvailabilitySlot)
class AvailabilitySlotAdmin(admin.ModelAdmin):
    list_display = ("id", "mentor", "start_at", "end_at", "is_active")
    list_filter = ("mentor", "is_active")
    ordering = ("start_at",)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "slot", "student", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("student__username", "slot__mentor__username")
