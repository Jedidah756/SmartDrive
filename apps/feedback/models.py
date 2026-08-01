from django.conf import settings
from django.db import models


class Feedback(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="feedback_entries")
    trip = models.ForeignKey("trips.Trip", on_delete=models.CASCADE, related_name="feedback_entries")
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()
    admin_response = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Feedback #{self.pk}"
