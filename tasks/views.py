from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django_filters.views import FilterView

from .filters import TaskFilter
from .models import Task
from .forms import TaskForm


class TaskListView(LoginRequiredMixin, FilterView):  # <-- FilterView вместо ListView
    model = Task
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'
    login_url = '/login/'
    filterset_class = TaskFilter

    def get_filterset_kwargs(self, filterset_class):
        kwargs = super().get_filterset_kwargs(filterset_class)
        kwargs['request'] = self.request
        return kwargs


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/detail.html'
    context_object_name = 'task'
    login_url = '/login/'


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks:index')
    login_url = '/login/'

    def form_valid(self, form):
        form.instance.author = self.request.user  # Автор = текущий пользователь
        response = super().form_valid(form)
        messages.success(self.request, 'Задача успешно создана')
        return response


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('tasks:index')
    login_url = '/login/'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Задача успешно изменена')
        return response


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks:index')
    login_url = '/login/'

    def test_func(self):
        # Удалять может только автор задачи
        task = self.get_object()
        return self.request.user == task.author

    def handle_no_permission(self):
        messages.error(self.request, 'Задачу может удалить только ее автор')
        return redirect('tasks:index')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Задача успешно удалена')
        return super().delete(request, *args, **kwargs)