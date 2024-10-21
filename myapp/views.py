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
    # Check if the user already has an appointment
    existing_appointment = Appointment.objects.filter(user=request.user).first()

    if existing_appointment:
        # If the user already has an appointment, display a message and redirect
        messages.error(request, "You already have an appointment.")
        return redirect('appointment_list')  # Redirect to the appointment list page

    if request.method == 'POST':
        form = AppointmentForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the form but don't commit yet
            appointment = form.save(commit=False)
            # Assign the current user to the appointment
            appointment.user = request.user
            appointment.save()
            messages.success(request, "Your appointment has been booked successfully.")
            return redirect('appointment_list')
    else:
        form = AppointmentForm()

    return render(request, 'book_appointment.html', {'form': form})

@login_required
def appointment_list(request):
    appointments = Appointment.objects.filter(user=request.user)
    return render(request, 'myapp/appointment_list.html', {'appointments': appointments})

@login_required
def booking_view(request):
    # Check if the user already has an appointment
    existing_appointment = Appointment.objects.filter(user=request.user).first()

    if existing_appointment:
        # If the user already has an appointment, display a message and redirect
        messages.error(request, "You already have an appointment.")
        return redirect('appointment_list')  # Redirect to the appointment list page

    if request.method == 'POST':
        form = AppointmentForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the form but don't commit yet
            appointment = form.save(commit=False)
            # Assign the current user to the appointment
            appointment.user = request.user
            appointment.save()
            messages.success(request, "Your appointment has been booked successfully.")
            return redirect('appointment_list')
    else:
        form = AppointmentForm()

    return render(request, 'myapp/booking.html', {'form': form})



def logout_view(request):
    logout(request)  # Log the user out
    return redirect('home')  # Redirect to home page or wherever you want
