from django.shortcuts import render, redirect, get_object_or_404
from .models import Appointment
from .forms import AppointmentForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
import csv
import logging



logger = logging.getLogger(__name__)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to home page after successful login
    else:
        form = AuthenticationForm()
    
    return render(request, 'registration/login.html', {'form': form})


def home(request):
    return render(request, 'myapp/home.html')

def about(request):
    return render(request, 'myapp/about.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'profile.html')

from datetime import datetime, timedelta
from django.utils import timezone

@login_required
def book_appointment(request):
    # Define restricted days (0=Monday, 6=Sunday) and times (in 24-hour format)
    restricted_days = [5, 6]  # For example, 5=Saturday, 6=Sunday
    restricted_times = [(18, 0), (20, 0)]  # Restrict appointments from 6 PM to 8 PM

    # Check if the user already has a future appointment
    existing_appointment = Appointment.objects.filter(user=request.user, date__gte=timezone.now().date()).first()

    if existing_appointment:
        messages.error(request, "You already have a future appointment. You cannot book more than one appointment.")
        return redirect('appointment_list')

    form = AppointmentForm()
    
    # Handle POST request for booking an appointment
    if request.method == 'POST':
        form = AppointmentForm(request.POST, request.FILES)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user  # Associate the appointment with the logged-in user

            # Check if the selected date is restricted
            appointment_day = appointment.date.weekday()  # Get the day of the week (0=Monday, 6=Sunday)
            appointment_time = (appointment.time.hour, appointment.time.minute)  # Get the time as a tuple
            
            # Check if the appointment falls on a restricted day or within restricted times
            if appointment_day in restricted_days:
                messages.error(request, "You cannot book appointments on weekends.")
                return redirect('book_appointment')

            # Check if appointment time is within restricted times
            for start_time in restricted_times:
                # Compare the start time (e.g., 18:00) with appointment time
                if appointment_time >= start_time and appointment_time < (start_time[0] + 1, 0):  # Check if it's within the hour
                    messages.error(request, "You cannot book appointments during restricted hours (6 PM to 8 PM).")
                    return redirect('book_appointment')

            appointment.save()  # Save the appointment
            messages.success(request, "Your appointment has been booked successfully.")
            return redirect('appointment_list')  # Redirect to the list of appointments

    # Render the booking form template
    return render(request, 'myapp/book_appointment.html', {'form': form})

@login_required
def appointment_list(request):
    appointments = Appointment.objects.filter(user=request.user).order_by('date')
    return render(request, 'myapp/appointment_list.html', {'appointments': appointments})  


def edit_appointment(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('owner_dashboard')
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'myapp/edit_appointment.html', {'form': form, 'appointment': appointment})

@login_required
def modify_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, user=request.user)
    
    if request.method == "POST":
        form = AppointmentForm(request.POST, request.FILES, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, "Your appointment has been updated successfully.")
            return redirect('appointment_list')
    else:
        form = AppointmentForm(instance=appointment)

    return render(request, 'myapp/modify_appointment.html', {'form': form, 'appointment': appointment})


@login_required
def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.delete()
    return redirect('appointment_list')  # Adjust this to your URL name for the appointment list.
        

def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.delete()
    return redirect('appointment_list')  #     

@login_required
def appointment_events(request):
    appointments = Appointment.objects.filter(user=request.user, date__gte=timezone.now().date())
    events = []

    for appointment in appointments:
        start_datetime = timezone.make_aware(timezone.datetime.combine(appointment.date, appointment.time))
        end_datetime = start_datetime + timezone.timedelta(hours=1)

        events.append({
            'title': appointment.description,
            'start': start_datetime.isoformat(),
            'end': end_datetime.isoformat(),
        })

    # Adding restrictions
    # For example, disabling weekends
    today = timezone.now().date()
    for i in range(7):  # Next 7 days
        date = today + timezone.timedelta(days=i)
        if date.weekday() in [5, 6]:  # Saturday and Sunday
            events.append({
                'title': 'Unavailable',
                'start': date.isoformat() + 'T00:00:00',
                'end': date.isoformat() + 'T23:59:59',
                'rendering': 'background',  # Render as background to indicate unavailable
            })
    
    # Example for lunch hours (12 PM - 1 PM)
    for appointment in appointments:
        start_lunch = timezone.datetime.combine(appointment.date, timezone.datetime.strptime("12:00", "%H:%M").time())
        end_lunch = start_lunch + timezone.timedelta(hours=1)

        events.append({
            'title': 'Lunch Hour - Unavailable',
            'start': start_lunch.isoformat(),
            'end': end_lunch.isoformat(),
            'rendering': 'background',
        })

    return JsonResponse(events, safe=False)

def export_appointments(request):
    appointments = Appointment.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="appointments.csv"'
    writer = csv.writer(response)
    writer.writerow(['Date', 'Notes'])
    for appointment in appointments:
        writer.writerow([appointment.date, appointment.notes])
    return response

class OwnerDashboardView(LoginRequiredMixin, TemplateView):
    def get(self, request):
        appointments = Appointment.objects.all()
        date_filter = request.GET.get('date')
        if date_filter:
            appointments = appointments.filter(date__date=date_filter)
        search_query = request.GET.get('search')
        if search_query:
            appointments = appointments.filter(notes__icontains=search_query)

        return render(request, 'myapp/owner_dashboard.html', {'appointments': appointments})

def logout_view(request):
    logout(request)
    return redirect('home')
