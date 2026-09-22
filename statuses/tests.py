from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Status

class StatusesCRUDTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123'
        )
        self.status = Status.objects.create(name='Новый')

    def test_create_status(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(reverse('statuses:create'), {
            'name': 'В работе'
        })
        self.assertRedirects(response, reverse('statuses:index'))
        self.assertTrue(Status.objects.filter(name='В работе').exists())

    def test_update_status(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(reverse('statuses:update', args=[self.status.pk]), {
            'name': 'Обновленный статус'
        })
        self.assertRedirects(response, reverse('statuses:index'))
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Обновленный статус')

    def test_delete_status(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(reverse('statuses:delete', args=[self.status.pk]))
        self.assertRedirects(response, reverse('statuses:index'))
        self.assertFalse(Status.objects.filter(name='Новый').exists())

    def test_unauthorized_access(self):
        response = self.client.get(reverse('statuses:index'))
        self.assertRedirects(response, f'/login/?next={reverse("statuses:index")}')