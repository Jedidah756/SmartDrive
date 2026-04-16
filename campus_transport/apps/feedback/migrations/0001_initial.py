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
            name="Feedback",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("rating", models.PositiveSmallIntegerField()),
                ("comment", models.TextField()),
                ("admin_response", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("student", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="feedback_entries", to="accounts.user")),
                ("trip", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="feedback_entries", to="trips.trip")),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
