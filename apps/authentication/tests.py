import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .views import login_view, create_user_view  # Adjust import path

User = get_user_model()

class AuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser(
            username='admin', email='admin@test.com', password='adminpass'
        )
        self.client.login(username='admin', password='adminpass')

    def test_login_success(self):
        # Test successful login with JSON-like data
        response = self.client.post(reverse('login'), data={
            'username': 'admin',
            'password': 'adminpass',
            'remember_me': 'on'
        })
        self.assertEqual(response.status_code, 302)  # Redirect on success
        self.assertTrue('_auth_user_id' in self.client.session)  # Session created

    def test_login_invalid_json(self):
        # Simulate invalid JSON payload (e.g., via API if view adapted)
        invalid_data = json.dumps({'username': 'wrong', 'password': 'wrong'})
        response = self.client.post(reverse('login'), data=invalid_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)  # Renders form with error
        self.assertContains(response, 'Invalid username or password')  # Check message

    def test_create_user_success(self):
        # Test creating user with valid POST data (form-like, but serialize to JSON for test)
        data = {
            'first_name': 'Test', 'last_name': 'User', 'username': 'testuser',
            'email': 'test@user.com', 'phone_number': '1234567890',
            'role': 'employee', 'password': 'testpass', 'confirm_password': 'testpass'
        }
        response = self.client.post(reverse('system_admin:create_user'), data=data)
        self.assertEqual(response.status_code, 302)  # Redirect on success
        new_user = User.objects.get(username='testuser')
        self.assertTrue(new_user.check_password('testpass'))

    def test_create_user_duplicate_email_json(self):
        # Create existing user first
        User.objects.create_user(username='existing', email='dup@test.com', password='pass')
        data = json.dumps({
            'first_name': 'Dup', 'last_name': 'User', 'username': 'dupuser',
            'email': 'dup@test.com', 'phone_number': '123', 'role': 'employee',
            'password': 'pass', 'confirm_password': 'pass'
        })
        response = self.client.post(reverse('system_admin:create_user'), data=data, content_type='application/json')
        self.assertEqual(response.status_code, 302)  # Redirect with error message
        # In view, it uses messages; test via response context or follow redirect

# Run with: python manage.py test