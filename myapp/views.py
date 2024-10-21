from django.shortcuts import render, redirect
from .models import Appointment
from .forms import AppointmentForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm
from django.contrib import messages
from django.utils import timezone
from django.shortcuts import get_object_or_404



def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to a success page
    else:
        form = AuthenticationForm()
    
    return render(request, 'registration/login.html', {'form': form})

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after successful registration
            return redirect('home')  # Redirect to the home page or any other page
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'profile.html')


@login_required
def book_appointment(request):
    # Check if the user has any future appointment
    existing_appointment = Appointment.objects.filter(user=request.user, date__gte=timezone.now().date()).first()

    if existing_appointment:
        # If the user has a future appointment, show an error message and redirect
        messages.error(request, "You already have a future appointment. You cannot book more than one appointment.")
        return redirect('appointment_list')  # Redirect to the user's appointment list page

    if request.method == 'POST':
        form = AppointmentForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the form but don't commit yet
            appointment = form.save(commit=False)
            # Assign the current user to the appointment
            appointment.user = request.user
            appointment.save()
            messages.success(request, "Your appointment has been booked successfully.")
            return redirect('appointment_list')  # Redirect after successful booking
    else:
        form = AppointmentForm()

    return render(request, 'myapp/book_appointment.html', {'form': form})


@login_required
def appointment_list(request):
    appointments = Appointment.objects.filter(user=request.user)
    return render(request, 'myapp/appointment_list.html', {'appointments': appointments})

@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, user=request.user)
    
    if request.method == "POST":
        appointment.delete()  # Delete the appointment
        messages.success(request, "Your appointment has been canceled.")
        return redirect('appointment_list')  # Redirect to appointment list
    
    return render(request, 'myapp/cancel_appointment.html', {'appointment': appointment})

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




def logout_view(request):
    logout(request)  # Log the user out
    return redirect('home')  # Redirect to home page or wherever you want
