from django.conf import settings
from django.db import models


class Trip(models.Model):
    class Status(models.TextChoices):
        SCHEDULED = "scheduled", "Scheduled"
        DEPARTED = "departed", "Departed"
        EN_ROUTE = "en_route", "En Route"
        ARRIVED = "arrived", "Arrived"
        DELAYED = "delayed", "Delayed"
        BREAKDOWN = "breakdown", "Breakdown"
        CANCELLED = "cancelled", "Cancelled"

    schedule = models.ForeignKey("schedules.Schedule", on_delete=models.CASCADE, related_name="trips")
    trip_date = models.DateField()
    scheduled_departure = models.TimeField()
    actual_departure = models.DateTimeField(blank=True, null=True)
    actual_arrival = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SCHEDULED)
    driver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="driven_trips")

    class Meta:
        ordering = ["-trip_date", "scheduled_departure"]
        unique_together = ("schedule", "trip_date")

    def __str__(self):
        return f"{self.schedule.route.name} - {self.trip_date}"


class TripUpdate(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="updates")
    status = models.CharField(max_length=20, choices=Trip.Status.choices)
    note = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.trip} - {self.status}"
