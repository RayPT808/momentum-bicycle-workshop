from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile

from myapp.models import Appointment


# Test for opening home page
class HomePageTest(TestCase):
    def test_home_page_status_code(self):
        """Test if home page loads successfully"""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)


# Test for login functionality
class LoginTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_login_success(self):
        """Test if login is successful and user is authenticated"""
        response = self.client.post(
            reverse("login"), {"username": "testuser", "password": "testpassword"}
        )
        self.assertEqual(response.status_code, 302)  # Expect redirect on successful login
        self.assertTrue(response.wsgi_request.user.is_authenticated)


# Test for new user registration function
class RegistrationTest(TestCase):
    def test_registration_success(self):
        """Test if user can register successfully"""
        response = self.client.post(
            reverse("register"),
            {
                "username": "newuser",
                "password1": "TestPassword123!",
                "password2": "TestPassword123!",
                "email": "newuser@example.com",
            },
        )

        self.assertTrue(User.objects.filter(username="newuser").exists())
        self.assertEqual(response.status_code, 302)

        user = User.objects.get(username="newuser")
        self.assertTrue(user.is_active)


# Test for logout function
class LogoutTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="TestPassword123!"
        )

    def test_logout_success(self):
        """Test if user can log out successfully"""
        self.client.login(username="testuser", password="TestPassword123!")

        response = self.client.post(reverse("logout"))

        self.assertEqual(response.status_code, 302)  # Expecting redirect

        response_after_logout = self.client.get(reverse("home"))
        self.assertNotIn("_auth_user_id", self.client.session)


# Test for booking an appointment
class AppointmentBookingTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")

    def test_appointment_booking(self):
        """Test if appointment booking is successful"""
        future_date = (timezone.now() + timedelta(days=1)).date()

        data = {
            "date": future_date.strftime("%Y-%m-%d"),
            "time": "09:00",
            "description": "Test appointment",
        }

        response = self.client.post(reverse("book_appointment"), data, follow=True)

        # Debugging info (optional, can be removed)
        print("Response status code:", response.status_code)
        if "form" in response.context:
            print("Form errors:", response.context["form"].errors)

        self.assertEqual(Appointment.objects.count(), 1)


# Test for deleting an appointment
class DeleteAppointmentTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")

        self.appointment = Appointment.objects.create(
            user=self.user,
            date=timezone.now().date(),
            time=timezone.now().time(),
            description="Test appointment",
        )

    def test_cancel_appointment(self):
        """Test if a user can cancel their appointment successfully"""
        response = self.client.post(
            reverse("delete_appointment", args=[self.appointment.id])
        )

        self.assertEqual(Appointment.objects.count(), 0)  # Appointment should be deleted
        self.assertEqual(response.status_code, 302)  # Expecting a redirect
