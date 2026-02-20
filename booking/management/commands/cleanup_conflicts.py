from django.core.management.base import BaseCommand
from booking.models import Booking
from django.db.models import Min

class Command(BaseCommand):
    help = "Cleanup duplicate 'booked' bookings per slot, keep earliest created."

    def handle(self, *args, **options):
        # za svaki slot pronađi najmanji created_at i ostavi samo taj; ostale postavi na 'cancelled'
        qs = Booking.objects.filter(status='booked')
        slot_ids = qs.values_list('slot', flat=True).distinct()
        changed = 0
        for slot_id in slot_ids:
            bookings = Booking.objects.filter(slot_id=slot_id, status='booked').order_by('created_at')
            if bookings.count() > 1:
                first = bookings.first()
                others = bookings.exclude(pk=first.pk)
                others.update(status='cancelled')
                changed += others.count()
        self.stdout.write(self.style.SUCCESS(f"Cancelled {changed} conflicting bookings."))
