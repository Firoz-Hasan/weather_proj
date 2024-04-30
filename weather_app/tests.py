
# tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class ViewTestCase(TestCase):
    def setUp(self):
        # Create a test user for authentication
        self.user = User.objects.create_user(username='hasan', password='qwer')

    def test_login_view(self):
        # Test login functionality with valid credentials
        response = self.client.post(reverse('login'), {'username': 'hasan', 'password': 'qwer'})
        self.assertEqual(response.status_code, 302)  # Redirects to index page upon successful login
        self.assertEqual(response.url, reverse('index'))  # Checks if redirected to index page

        # Test login functionality with invalid credentials
        response = self.client.post(reverse('login'), {'username': 'invaliduser', 'password': 'invalidpassword'})
        self.assertEqual(response.status_code, 200)  # Returns to login page upon failed login
        self.assertContains(response, 'Invalid username or password')  # Checks if error message is displayed

    def test_register_view(self):
        # Test registration functionality with valid credentials
        response = self.client.post(reverse('register'), {'username': 'newuser', 'password': 'newpassword', 'confirm_password': 'newpassword'})
        self.assertEqual(response.status_code, 302)  # Redirects to login page upon successful registration
        self.assertEqual(response.url, reverse('login'))  # Checks if redirected to login page

        # Test registration functionality with existing username
        response = self.client.post(reverse('register'), {'username': 'testuser', 'password': 'newpassword', 'confirm_password': 'newpassword'})
        self.assertEqual(response.status_code, 302)  # Redirects to register page upon existing username
        self.assertEqual(response.url, reverse('register'))  # Checks if redirected to register page

        # Test registration functionality with mismatched passwords
        response = self.client.post(reverse('register'), {'username': 'anotheruser', 'password': 'password1', 'confirm_password': 'password2'})
        self.assertEqual(response.status_code, 302)  # Redirects to register page upon mismatched passwords
        self.assertEqual(response.url, reverse('register'))  # Checks if redirected to register page

    def test_index_view(self):
        # Test index view when user is authenticated
        self.client.force_login(self.user)
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)  # Checks if index page is accessible
        self.assertTemplateUsed(response, 'index.html')  # Checks if correct template is used

        # Test index view when user is not authenticated
        self.client.logout()
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)  # Checks if index page is accessible
        self.assertTemplateUsed(response, 'index.html')  # Checks if correct template is used
# python manage.py test
