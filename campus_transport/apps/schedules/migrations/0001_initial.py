from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("accounts", "0001_initial"),
        ("routes", "0001_initial"),
        ("vehicles", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Schedule",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("departure_time", models.TimeField()),
                ("days_of_week", models.JSONField(default=list)),
                ("status", models.CharField(choices=[("active", "Active"), ("paused", "Paused"), ("inactive", "Inactive")], default="active", max_length=20)),
                ("driver", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="assigned_schedules", to="accounts.user")),
                ("route", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="schedules", to="routes.route")),
                ("vehicle", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="schedules", to="vehicles.vehicle")),
            ],
            options={"ordering": ["departure_time"]},
        ),
    ]
