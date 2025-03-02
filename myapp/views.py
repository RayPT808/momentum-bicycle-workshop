from django.shortcuts import render, redirect, get_object_or_404
from myapp.models import Appointment, Notification
from django.core.mail import send_mail
from .forms import ProfileForm, UserForm
from .models import Profile
from .forms import AppointmentForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.views.generic import TemplateView, View  #
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import now
import csv
import logging
from django.template.loader import get_template

def some_view(request):
    return render(request, 'myapp/base.html', {'timestamp': now().timestamp()})
    

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
    template_path = "myapp/home.html"
    try:
        get_template(template_path)  # Raises an error if not found
        return render(request, template_path, {'page_title': 'Home'})
    except Exception as e:
        return HttpResponse(f"❌ Template error: {e}")


def contact(request):
    template_path = "myapp/contact.html"
    try:
        get_template(template_path)
        return render(request, template_path, {'page_title': 'Contact'})
    except Exception as e:
        return HttpResponse(f"❌ Template error: {e}")


    

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
def profile_view(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')  # Reload profile page

    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    # Fix: Replace status with completed
    completed_appointments = Appointment.objects.filter(user=user, completed=True)

    return render(request, 'myapp/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'completed_appointments': completed_appointments,
        'username': user.username
    })


@login_required
def user_dashboard(request):
    # Get the notifications for the logged-in user
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')

    # Debugging log
    print(f"Notifications for {request.user.username}: {notifications}")

    
    # Render the user dashboard template with notifications
    return render(request, 'user_dashboard.html', {'notifications': notifications})

@login_required
def book_appointment(request):
    restricted_days = [5, 6]  # 5 = Saturday, 6 = Sunday
    valid_start_hour = 8  # 8 AM
    valid_end_hour = 18  # 6 PM (exclusive)

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
            appointment_hour = appointment.time.hour
            appointment_minute = appointment.time.minute

            # Ensure the time is at the start of the hour (e.g., 1:00, 2:00)
            if appointment_minute != 0:
                messages.error(request, "You can only book appointments at the start of the hour (e.g., 1:00, 2:00).")
                return redirect('book_appointment')

            # Ensure appointments are not on restricted days
            if appointment_day in restricted_days:
                messages.error(request, "You cannot book appointments on weekends.")
                return redirect('book_appointment')

            # Ensure the hour is within the allowed range
            if not (valid_start_hour <= appointment_hour < valid_end_hour):
                messages.error(request, "You can only book appointments between 8 AM and 6 PM.")
                return redirect('book_appointment')

            # Save the appointment
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
    
    # Update column headers based on the actual fields in the model
    writer.writerow(['User', 'Date', 'Time', 'Description', 'Photo'])  # Column headers to reflect available fields
    
    for appointment in appointments:
        # Write the available fields (remove the `notes` field)
        writer.writerow([
            appointment.user.username,  # User
            appointment.date,           # Date
            appointment.time,           # Time
            appointment.description,     # Description (equivalent of notes)
            appointment.photo.url if appointment.photo else ''  # Photo URL, or empty string if no photo
        ])
    
    return response


class OwnerDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'myapp/owner_dashboard.html'
    
    def get(self, request):
        appointments = Appointment.objects.all()

        # Apply date filter if present
        date_filter = request.GET.get('date')
        if date_filter:
            appointments = appointments.filter(date=date_filter)

        
        # Apply search filter if present
        search_query = request.GET.get('search')
        if search_query:
            appointments = appointments.filter(description__icontains=search_query)
        
        # Include the list of appointments in the context
        return render(request, self.template_name, {'appointments': appointments})

# New view for marking an appointment as completed
@login_required
def mark_appointment_completed(request, appointment_id):
    print(f"Marking appointment {appointment_id} as completed.")
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Mark the appointment as completed
    appointment.completed = True
    appointment.notified = True 
    appointment.save()

    user_notification = Notification.objects.create(
    user=appointment.user,
    message=f"Your appointment on {appointment.date} at {appointment.time} has been marked as completed.",
    read=False,  # This means the notification hasn't been viewed yet
  
)
    print(f"Notification created: {user_notification}")

    # Add a success message for the shop owner
    messages.success(request, f"Your appointment on {appointment.date} at {appointment.time} has been marked as completed.")

   
    # Provide feedback to the owner
    messages.success(request, f"Appointment for {appointment.user.username} marked as completed and user notified.")

    # Redirect back to the owner dashboard and re-fetch the updated appointments
    return redirect('owner_dashboard')
