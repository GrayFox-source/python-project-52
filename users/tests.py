from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class UsersCRUDTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123',
            first_name='Test',
            last_name='User'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='otherpassword123'
        )

    def test_create_user(self):
        response = self.client.post(reverse('users:create'), {
            'first_name': 'New',
            'last_name': 'User',
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        })
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_update_own_user(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(reverse('users:update', args=[self.user.pk]), {
            'first_name': 'Updated',
            'last_name': 'Name',
            'username': 'testuser'
        })
        self.assertRedirects(response, reverse('users:index'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')

    def test_update_other_user_forbidden(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(reverse('users:update', args=[self.other_user.pk]), {
            'first_name': 'Hacked',
            'last_name': 'Name',
            'username': 'otheruser'
        })
        # Должен редиректить на список с ошибкой
        self.assertRedirects(response, reverse('users:index'))
        self.other_user.refresh_from_db()
        self.assertNotEqual(self.other_user.first_name, 'Hacked')

    def test_delete_own_user(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(reverse('users:delete', args=[self.user.pk]))
        self.assertRedirects(response, reverse('users:index'))
        self.assertFalse(User.objects.filter(username='testuser').exists())