import django_filters
from django import forms
from django.contrib.auth.models import User

from labels.models import Label
from statuses.models import Status

from .models import Task


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        label='Статус',
        empty_label='Не выбрано',
        field_name='status'
    )

    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label='Исполнитель',
        empty_label='Не выбрано',
        field_name='executor'
    )

    labels = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        label='Метка',
        empty_label='Не выбрано',
        field_name='labels'
    )

    only_own = django_filters.BooleanFilter(
        method='filter_only_own',
        label='Только свои задачи',
        widget=forms.CheckboxInput()
    )

    class Meta:
        model = Task
        fields = []

    def filter_only_own(self, queryset, name, value):
        if value and str(value).lower() in ['true', '1'] and self.request and self.request.user.is_authenticated:
            return queryset.filter(author=self.request.user)
        return queryset