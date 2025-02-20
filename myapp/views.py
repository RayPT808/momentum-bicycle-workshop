from django.shortcuts import render, redirect, get_object_or_404
from .models import Appointment
from .forms import AppointmentForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.views.generic import TemplateView, View  # Import View
from django.contrib.auth.mixins import LoginRequiredMixin
import csv
import logging

logger = logging.getLogger(__name__)

class CustomLogoutView(View):
    def post(self, request):
        logout(request)
        return redirect('home')

        
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

@login_required
def book_appointment(request):
    restricted_days = [5, 6]  # For example, 5=Saturday, 6=Sunday
    valid_start_time = (8, 0)  # 8 AM
    valid_end_time = (18, 0)   # 6 PM

    existing_appointment = Appointment.objects.filter(user=request.user, date__gte=timezone.now().date()).first()

    if existing_appointment:
        messages.error(request, "You already have a future appointment. You cannot book more than one appointment.")
        return redirect('appointment_list')

    form = AppointmentForm()
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST, request.FILES)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user

            appointment_day = appointment.date.weekday()
            appointment_time = (appointment.time.hour, appointment.time.minute)

            if appointment.time.minute != 0:
                messages.error(request, "You can only book appointments on the hour (e.g., 1:00, 2:00).")
                return redirect('book_appointment')
            
            if appointment_day in restricted_days:
                messages.error(request, "You cannot book appointments on weekends.")
                return redirect('book_appointment')

            if not (valid_start_time <= appointment_time < valid_end_time):
                messages.error(request, "You can only book appointments between 8 AM and 6 PM.")
                return redirect('book_appointment')

            appointment.save()
            messages.success(request, "Your appointment has been booked successfully.")
            return redirect('appointment_list')

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
def delete_appointment(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    
    if request.method == 'POST':
        appointment.delete()
        messages.success(request, 'Appointment deleted successfully.')
        return redirect('appointment_list')

    return redirect('appointment_list')

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

    today = timezone.now().date()
    for i in range(7):
        date = today + timezone.timedelta(days=i)
        if date.weekday() in [5, 6]:
            events.append({
                'title': 'Unavailable',
                'start': date.isoformat() + 'T00:00:00',
                'end': date.isoformat() + 'T23:59:59',
                'rendering': 'background',
            })
    
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
