from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.username


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message


class Appointment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE
    )  # Associate the appointment with a user
    date = models.DateField()
    time = models.TimeField()
    description = models.TextField(blank=True)  # Allowing blank descriptions
    photo = models.ImageField(upload_to="photos/", blank=True, null=True)
    completed = models.BooleanField(default=False)
    notified = models.BooleanField(default=False)

    def clean(self):
        # Ensure the appointment date and time are not None
        if not self.date or not self.time:
            raise ValidationError("Date and time must be set.")

        # Ensure the appointment date and time are not in the past
        appointment_datetime = timezone.make_aware(
            timezone.datetime.combine(self.date, self.time)
        )
        if appointment_datetime < timezone.now():
            raise ValidationError("The appointment cannot be in the past.")

    def __str__(self):
        return f"{self.user.username} - {self.date} at {self.time}"

    class Meta:
        unique_together = (
            "user",
            "date",
        )  # or ('user', 'date', 'time') if you want to prevent double booking at the same time
