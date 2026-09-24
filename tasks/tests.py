from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from labels.models import Label
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



class TaskFilterTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser', password='otherpassword123'
        )
        self.status_new = Status.objects.create(name='Новый')
        self.status_done = Status.objects.create(name='Завершен')
        self.label_bug = Label.objects.create(name='Баг')

        self.task1 = Task.objects.create(
            name='Задача 1',
            status=self.status_new,
            author=self.user,
            executor=self.user
        )
        self.task1.labels.add(self.label_bug)

        self.task2 = Task.objects.create(
            name='Задача 2',
            status=self.status_done,
            author=self.other_user,
            executor=self.other_user
        )

    def test_filter_by_status(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('tasks:index'), {'status': self.status_new.pk})
        self.assertEqual(response.status_code, 200)
        tasks = response.context['tasks']
        self.assertTrue(all(t.status == self.status_new for t in tasks))

    def test_filter_by_executor(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('tasks:index'), {'executor': self.user.pk})
        self.assertEqual(response.status_code, 200)
        tasks = response.context['tasks']
        self.assertTrue(all(t.executor == self.user for t in tasks))

    def test_filter_by_label(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('tasks:index'), {'labels': self.label_bug.pk})
        self.assertEqual(response.status_code, 200)
        tasks = response.context['tasks']
        self.assertTrue(any(self.label_bug in t.labels.all() for t in tasks))

    def test_filter_only_own_tasks(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('tasks:index'), {'only_own': 'True'})
        self.assertEqual(response.status_code, 200)
        tasks = response.context['tasks']
        self.assertTrue(all(t.author == self.user for t in tasks))

    def test_combined_filters(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('tasks:index'), {
            'status': self.status_new.pk,
            'only_own': 'True'
        })
        self.assertEqual(response.status_code, 200)
        tasks = response.context['tasks']
        self.assertTrue(all(t.author == self.user and t.status == self.status_new for t in tasks))