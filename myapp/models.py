from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Associate the appointment with a user
    date = models.DateField()
    time = models.TimeField()
    description = models.TextField()
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)

    def clean(self):
        # Ensure the appointment date and time are not in the past
        appointment_datetime = timezone.make_aware(timezone.datetime.combine(self.date, self.time))
        if appointment_datetime < timezone.now():
            raise ValidationError("The appointment cannot be in the past.")
    
    def __str__(self):
        return f"{self.user.username} - {self.date} at {self.time}"
    
    class Meta:  # This should be properly indented within the model
        unique_together = ('user', 'date')  # or ('user', 'date', 'time') if you want to prevent double booking at the same time
