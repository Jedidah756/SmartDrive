from django.conf import settings
from django.db import models


class SmsNotification(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        SENT = "sent", "Sent"
        FAILED = "failed", "Failed"

    class Trigger(models.TextChoices):
        TRIP_DELAYED = "trip_delayed", "Trip Delayed"
        TRIP_CANCELLED = "trip_cancelled", "Trip Cancelled"
        TRIP_DEPARTED = "trip_departed", "Trip Departed"
        TRIP_ARRIVED = "trip_arrived", "Trip Arrived"
        BREAKDOWN = "breakdown", "Breakdown"

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sms_notifications")
    trip = models.ForeignKey("trips.Trip", on_delete=models.CASCADE, related_name="sms_notifications")
    trigger = models.CharField(max_length=32, choices=Trigger.choices)
    message = models.TextField()
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.SENT)
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-sent_at"]

    def __str__(self):
        return f"SMS to {self.recipient.name} — {self.get_trigger_display()}"
