from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from statuses.models import Status
from tasks.models import Task

from .models import Label


class LabelsCRUDTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword123'
        )
        self.status = Status.objects.create(name='Новый')
        self.label = Label.objects.create(name='Баг')
        self.task = Task.objects.create(
            name='Тестовая задача',
            status=self.status,
            author=self.user
        )
        self.task.labels.add(self.label)

    def test_create_label(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(reverse('labels:create'), {
            'name': 'Фича'
        })
        self.assertRedirects(response, reverse('labels:index'))
        self.assertTrue(Label.objects.filter(name='Фича').exists())

    def test_update_label(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(reverse('labels:update', args=[self.label.pk]), {
            'name': 'Критический баг'
        })
        self.assertRedirects(response, reverse('labels:index'))
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'Критический баг')

    def test_delete_label_without_tasks(self):
        # Создаем метку без задач
        unused_label = Label.objects.create(name='Не используется')
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(reverse('labels:delete', args=[unused_label.pk]))
        self.assertRedirects(response, reverse('labels:index'))
        self.assertFalse(Label.objects.filter(name='Не используется').exists())

    def test_delete_label_with_tasks_forbidden(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(reverse('labels:delete', args=[self.label.pk]))
        # Должен редиректить на список меток с ошибкой
        self.assertRedirects(response, reverse('labels:index'))
        # Метка должна остаться
        self.assertTrue(Label.objects.filter(name='Баг').exists())

    def test_unauthorized_access(self):
        response = self.client.get(reverse('labels:index'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)