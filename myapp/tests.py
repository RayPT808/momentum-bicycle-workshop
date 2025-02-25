from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from myapp.models import Appointment
from django.core.files.uploadedfile import SimpleUploadedFile



# Test for opening home page
class HomePageTest(TestCase):
    def test_home_page_status_code(self):
        """Test if home page loads successfully"""
        response = self.client.get(reverse('home'))  
        self.assertEqual(response.status_code, 200)


# Test for login functionality
class LoginTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_login_success(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)  # Expect redirect on successful login
        self.assertTrue(response.wsgi_request.user.is_authenticated)


# Test for new user registration function
class RegistrationTest(TestCase):
    def test_registration_success(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'TestPassword123!',
            'password2': 'TestPassword123!',
            'email': 'newuser@example.com'
        })

    
        self.assertTrue(User.objects.filter(username='newuser').exists())

        
        self.assertEqual(response.status_code, 302)

        
        user = User.objects.get(username='newuser')
        self.assertTrue(user.is_active)

# Test for logout function
class LogoutTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='TestPassword123!')

    def test_logout_success(self):
        self.client.login(username='testuser', password='TestPassword123!')

        response = self.client.get(reverse('logout'))  

        self.assertEqual(response.status_code, 302)

        response_after_logout = self.client.get(reverse('home'))  
        self.assertNotIn('_auth_user_id', self.client.session)


class AppointmentBookingTest(TestCase):

    def test_appointment_booking(self):
        # Data for the appointment form (without photo for simplicity)
        data = {
            'date': '2025-02-28',
            'time': '10:00',
            'description': 'Test appointment description',
        }

        # If you want to test photo upload, use this:
        # file = SimpleUploadedFile('test_image.jpg', b'file_content', content_type='image/jpeg')
        # data['photo'] = file

        # Send POST request to the appointment booking page
        response = self.client.post(reverse('book_appointment'), data)

        # Check if the appointment has been created
        self.assertEqual(Appointment.objects.count(), 1)
        # Check if the redirection happens after successful submission
        self.assertRedirects(response, reverse('home'))

        # Check if the data was correctly saved in the Appointment model
        appointment = Appointment.objects.first()
        self.assertEqual(appointment.date, '2025-02-28')
        self.assertEqual(appointment.time, '10:00')
        self.assertEqual(appointment.description, 'Test appointment description')
        # If testing with a photo:
        # self.assertTrue(appointment.photo.name.endswith('test_image.jpg'))