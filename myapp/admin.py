from django.contrib import admin
from .models import Appointment  # Import your models here

from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    # Here is where you define the list_display
    list_display = ('user', 'date', 'time', 'description', 'photo')  # Add photo to the displayed fields
    list_filter = ('date', 'user')  # Optional: filters for sidebar
    search_fields = ('user__username', 'description')  # Optional: fields to search by

    # You can also customize the fields displayed in the form when editing an appointment
    fields = ('user', 'date', 'time', 'description', 'photo')  # Adjust as needed

# Additional customizations can go here
