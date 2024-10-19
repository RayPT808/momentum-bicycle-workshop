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
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.save()
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
    if request.method == 'POST':
        date = request.POST.get('appointment_date')
        time = request.POST.get('appointment_time')
        notes = request.POST.get('notes')

        # Create a new Appointment object
        appointment = Appointment(
            user=request.user,
            date=date,
            time=time,
            notes=notes
        )
        appointment.save()

        # Redirect to a success page or back to the booking page
        return redirect('booking_success')  # Create this URL pattern

    return render(request, 'myapp/booking.html')  # Adjust this path as necessary

def logout_view(request):
    logout(request)  # Log the user out
    return redirect('home')  # Redirect to home page or wherever you want
