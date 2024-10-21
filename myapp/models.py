from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Associate the appointment with a user
    date = models.DateField()
    time = models.TimeField()
    description = models.TextField()
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.date} at {self.time}"