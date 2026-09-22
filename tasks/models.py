from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from statuses.models import Status
from labels.models import Label


# Create your models here.

class Task(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Имя')
    description = models.TextField(blank=True, default='', verbose_name='Описание')
    status = models.ForeignKey(
        Status, on_delete=models.PROTECT, verbose_name='Статус'
    )
    author = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='author_tasks',
        verbose_name='Автор'
    )
    executor = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='executor_tasks', verbose_name='Исполнитель'
    )
    labels = models.ManyToManyField(
        Label, blank=True, related_name='tasks', verbose_name='Метки'
    )
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
