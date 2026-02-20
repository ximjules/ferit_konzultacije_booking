from django.conf import settings
from django.db import models
from django.utils import timezone

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
    """
    Rezervacija termina. Povezana na AvailabilitySlot.
    """
    STATUS_CHOICES = [
        ('booked', 'Booked'),
        ('cancelled', 'Cancelled'),
    ]

    slot = models.ForeignKey(
        'AvailabilitySlot',
        on_delete=models.CASCADE,
        related_name='bookings',
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings',
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='booked')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.student} -> {self.slot} ({self.status})"
