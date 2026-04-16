from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("accounts", "0001_initial"),
        ("schedules", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Trip",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("trip_date", models.DateField()),
                ("scheduled_departure", models.TimeField()),
                ("actual_departure", models.DateTimeField(blank=True, null=True)),
                ("actual_arrival", models.DateTimeField(blank=True, null=True)),
                ("status", models.CharField(choices=[("scheduled", "Scheduled"), ("departed", "Departed"), ("en_route", "En Route"), ("arrived", "Arrived"), ("delayed", "Delayed"), ("breakdown", "Breakdown"), ("cancelled", "Cancelled")], default="scheduled", max_length=20)),
                ("driver", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="driven_trips", to="accounts.user")),
                ("schedule", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="trips", to="schedules.schedule")),
            ],
            options={"ordering": ["-trip_date", "scheduled_departure"], "unique_together": {("schedule", "trip_date")}},
        ),
        migrations.CreateModel(
            name="TripUpdate",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("status", models.CharField(choices=[("scheduled", "Scheduled"), ("departed", "Departed"), ("en_route", "En Route"), ("arrived", "Arrived"), ("delayed", "Delayed"), ("breakdown", "Breakdown"), ("cancelled", "Cancelled")], max_length=20)),
                ("note", models.TextField(blank=True)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                ("latitude", models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True)),
                ("longitude", models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True)),
                ("trip", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="updates", to="trips.trip")),
            ],
            options={"ordering": ["-timestamp"]},
        ),
    ]
