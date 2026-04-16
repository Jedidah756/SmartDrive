from django.db import models


class Route(models.Model):
    name = models.CharField(max_length=120, unique=True)
    start_point = models.CharField(max_length=120)
    end_point = models.CharField(max_length=120)
    stops_json = models.JSONField(default=list)
    distance_km = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
