from django.contrib import admin
from .models import Appointment  # Import your models here

from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):

    list_display = ('user', 'date', 'time', 'description', 'photo') 
    list_filter = ('date', 'user') 
    search_fields = ('user__username', 'description') 

    
    fields = ('user', 'date', 'time', 'description', 'photo') 


