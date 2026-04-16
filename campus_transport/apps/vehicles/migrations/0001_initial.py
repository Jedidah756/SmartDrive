from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Vehicle",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("plate_number", models.CharField(max_length=20, unique=True)),
                ("model", models.CharField(max_length=120)),
                ("capacity", models.PositiveIntegerField()),
                ("status", models.CharField(choices=[("active", "Active"), ("maintenance", "Maintenance"), ("inactive", "Inactive")], default="active", max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["plate_number"]},
        ),
    ]
