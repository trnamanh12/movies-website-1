from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class UserViewsTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user.save()

    def test_register_view(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Registered successfully, congratulations! Please login.')

    def test_login_view(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)  # Redirects to profile
        self.assertRedirects(response, reverse('profile'))

    def test_logout_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirects to login
        self.assertRedirects(response, reverse('home'))

    def test_view_profile(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')

    def test_edit_profile(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('edit_profile'), {
            'username': 'updateduser',
            'email': 'updateduser@example.com'
        })
        self.assertEqual(response.status_code, 302)  # Redirects to profile
        self.assertRedirects(response, reverse('profile'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')
        self.assertEqual(self.user.email, 'updateduser@example.com')

    def test_delete_account(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('delete_account'), {
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)  # Redirects to home
        self.assertRedirects(response, reverse('home'))
        self.assertFalse(User.objects.filter(username='testuser').exists())