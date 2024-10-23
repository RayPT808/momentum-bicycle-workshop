# Generated by Django 4.2.16 on 2024-10-21 15:09

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("myapp", "0003_remove_appointment_created_at_and_more"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="appointment",
            unique_together={("user", "date")},
        ),
    ]