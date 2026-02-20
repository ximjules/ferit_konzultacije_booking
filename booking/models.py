from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


class AvailabilitySlot(models.Model):
    mentor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="availability_slots"
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

    def clean(self):
        # Provjere prije spremanja
        if not self.slot.is_active:
            raise ValidationError("Cannot book an inactive slot.")
        if self.slot.start_at <= timezone.now():
            raise ValidationError("Cannot book a slot in the past.")
        qs = Booking.objects.filter(slot=self.slot, status='booked')
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        if qs.exists():
            raise ValidationError("This slot is already booked.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['slot'], name='unique_booking_per_slot'),
        ]
