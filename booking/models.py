from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class AvailabilitySlot(models.Model):
    mentor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="availability_slots"
    )
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["start_at"]
        constraints = [
            models.CheckConstraint(
                check=models.Q(end_at__gt=models.F("start_at")),
                name="slot_end_after_start",
            ),
        ]

    def __str__(self):
        return f"{self.mentor} | {self.start_at:%Y-%m-%d %H:%M} - {self.end_at:%H:%M}"


class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"
        CANCELLED = "CANCELLED", "Cancelled"
        COMPLETED = "COMPLETED", "Completed"

    slot = models.OneToOneField(
        AvailabilitySlot, on_delete=models.CASCADE, related_name="booking"
    )
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bookings"
    )

    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )

    student_note = models.TextField(blank=True)
    mentor_note = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.student} -> {self.slot} ({self.status})"
