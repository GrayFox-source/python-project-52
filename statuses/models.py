from django.db import models
from django.utils import timezone

# Create your models here.


class Status(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Имя')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']