# Generated by Django 5.1.6 on 2025-03-02 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0009_profile"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="address",
            field=models.TextField(blank=True, null=True),
        ),
    ]
