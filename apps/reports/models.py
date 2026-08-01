from django.conf import settings
from django.db import models


class Report(models.Model):
    class Type(models.TextChoices):
        DAILY_SUMMARY = "daily_summary", "Daily Summary"
        MONTHLY_USAGE = "monthly_usage", "Monthly Usage"
        DRIVER_PERFORMANCE = "driver_performance", "Driver Performance"
        ROUTE_UTILIZATION = "route_utilization", "Route Utilization"
        INCIDENT_LOG = "incident_log", "Incident Log"

    report_type = models.CharField(max_length=32, choices=Type.choices)
    date_range_start = models.DateField()
    date_range_end = models.DateField()
    generated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="generated_reports")
    file_path = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_report_type_display()} ({self.date_range_start} - {self.date_range_end})"
