from django.conf import settings
from django.db import models


class Incident(models.Model):
    class Severity(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"
        CRITICAL = "critical", "Critical"

    class Category(models.TextChoices):
        ACCIDENT = "accident", "Accident"
        BREAKDOWN = "breakdown", "Breakdown"
        DELAY = "delay", "Delay"
        OTHER = "other", "Other"

    trip = models.ForeignKey("trips.Trip", on_delete=models.CASCADE, related_name="incidents")
    driver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="incidents")
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.OTHER)
    description = models.TextField()
    severity = models.CharField(max_length=20, choices=Severity.choices, default=Severity.MEDIUM)
    reported_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-reported_at"]

    def __str__(self):
        return f"Incident #{self.pk}"
