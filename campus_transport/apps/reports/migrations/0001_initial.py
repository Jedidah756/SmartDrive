from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Report",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("report_type", models.CharField(choices=[("daily_summary", "Daily Summary"), ("monthly_usage", "Monthly Usage"), ("driver_performance", "Driver Performance"), ("route_utilization", "Route Utilization"), ("incident_log", "Incident Log")], max_length=32)),
                ("date_range_start", models.DateField()),
                ("date_range_end", models.DateField()),
                ("file_path", models.CharField(blank=True, max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("generated_by", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="generated_reports", to="accounts.user")),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
