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
            name="Incident",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("description", models.TextField()),
                ("severity", models.CharField(choices=[("low", "Low"), ("medium", "Medium"), ("high", "High"), ("critical", "Critical")], default="medium", max_length=20)),
                ("reported_at", models.DateTimeField(auto_now_add=True)),
                ("driver", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="incidents", to="accounts.user")),
                ("trip", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="incidents", to="trips.trip")),
            ],
            options={"ordering": ["-reported_at"]},
        ),
    ]
