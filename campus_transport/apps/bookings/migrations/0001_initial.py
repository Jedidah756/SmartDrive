from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("accounts", "0001_initial"),
        ("trips", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Booking",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("seat_number", models.PositiveIntegerField()),
                ("status", models.CharField(choices=[("reserved", "Reserved"), ("cancelled", "Cancelled"), ("completed", "Completed")], default="reserved", max_length=20)),
                ("booked_at", models.DateTimeField(auto_now_add=True)),
                ("student", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="bookings", to="accounts.user")),
                ("trip", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="bookings", to="trips.trip")),
            ],
            options={"ordering": ["-booked_at"], "unique_together": {("trip", "seat_number")}},
        ),
    ]
