from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from statuses.models import Status
from .models import Task


class TasksCRUDTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser', password='otherpassword123'
        )
        self.status = Status.objects.create(name='Новый')
        self.task = Task.objects.create(
            name='Тестовая задача',
            status=self.status,
            author=self.user
        )

    def test_create_task(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(reverse('tasks:create'), {
            'name': 'Новая задача',
            'description': 'Описание',
            'status': self.status.pk,
        })
        self.assertRedirects(response, reverse('tasks:index'))
        self.assertTrue(Task.objects.filter(name='Новая задача').exists())

    def test_update_task(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(reverse('tasks:update', args=[self.task.pk]), {
            'name': 'Обновлённая задача',
            'description': '',
            'status': self.status.pk,
        })
        self.assertRedirects(response, reverse('tasks:index'))
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Обновлённая задача')

    def test_delete_by_author(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(reverse('tasks:delete', args=[self.task.pk]))
        self.assertRedirects(response, reverse('tasks:index'))
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())

    def test_delete_by_non_author(self):
        self.client.login(username='otheruser', password='otherpassword123')
        response = self.client.post(reverse('tasks:delete', args=[self.task.pk]))
        # Должен редиректить на список задач с ошибкой
        self.assertRedirects(response, reverse('tasks:index'))
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())

    def test_unauthorized_access(self):
        response = self.client.get(reverse('tasks:index'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)