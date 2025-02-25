from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class HomePageTest(TestCase):
    def test_home_page_status_code(self):
        """Test if home page loads successfully"""
        response = self.client.get(reverse('home'))  
        self.assertEqual(response.status_code, 200)


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