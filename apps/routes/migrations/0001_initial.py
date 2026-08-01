from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Route",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120, unique=True)),
                ("start_point", models.CharField(max_length=120)),
                ("end_point", models.CharField(max_length=120)),
                ("stops_json", models.JSONField(default=list)),
                ("distance_km", models.DecimalField(decimal_places=2, max_digits=6)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["name"]},
        ),
    ]
