from django.conf import settings
from django.db import models


class Schedule(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        PAUSED = "paused", "Paused"
        INACTIVE = "inactive", "Inactive"

    route = models.ForeignKey("routes.Route", on_delete=models.CASCADE, related_name="schedules")
    vehicle = models.ForeignKey("vehicles.Vehicle", on_delete=models.CASCADE, related_name="schedules")
    driver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="assigned_schedules")
    departure_time = models.TimeField()
    days_of_week = models.JSONField(default=list)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)

    class Meta:
        ordering = ["departure_time"]

    def __str__(self):
        return f"{self.route.name} - {self.departure_time}"
