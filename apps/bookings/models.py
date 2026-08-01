from django.conf import settings
from django.db import models


class Booking(models.Model):
    class Status(models.TextChoices):
        RESERVED = "reserved", "Reserved"
        CANCELLED = "cancelled", "Cancelled"
        COMPLETED = "completed", "Completed"

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings")
    trip = models.ForeignKey("trips.Trip", on_delete=models.CASCADE, related_name="bookings")
    seat_number = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.RESERVED)
    booked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-booked_at"]
        unique_together = ("trip", "seat_number")

    def __str__(self):
        return f"{self.student.name} - Seat {self.seat_number}"
