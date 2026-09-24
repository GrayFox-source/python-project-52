import sys
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect

from .forms import CustomUserCreationForm, UserUpdateForm


class UserListView(ListView):
    model = User
    template_name = 'users/index.html'
    context_object_name = 'users'


class UserCreateView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/create.html'
    success_url = '/login/'

    def form_valid(self, form):
        messages.success(self.request, 'Пользователь успешно зарегистрирован')
        return super().form_valid(form)

    def form_invalid(self, form):
        # ВРЕМЕННЫЙ ДЕБАГ: выведет ошибки в логи GitHub Actions
        print(f"DEBUG FORM ERRORS: {form.errors}", file=sys.stderr)
        print(f"DEBUG FORM DATA: {self.request.POST}", file=sys.stderr)
        return super().form_invalid(form)


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users:index')

    def test_func(self):
        return self.request.user.pk == self.get_object().pk

    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет прав для изменения')
        return redirect('users:index')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Пользователь успешно изменен')
        return response


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users:index')

    def test_func(self):
        return self.request.user.pk == self.get_object().pk

    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет прав для изменения')
        return redirect('users:index')

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        if user.author_tasks.exists() or user.executor_tasks.exists():
            messages.error(self.request, 'Невозможно удалить пользователя')
            return redirect('users:index')

        messages.success(self.request, 'Пользователь успешно удален')
        return super().delete(request, *args, **kwargs)


class CustomLoginView(LoginView):
    template_name = 'users/login.html'

    def form_valid(self, form):
        messages.success(self.request, 'Вы залогинены')
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    next_page = '/'

    def dispatch(self, request, *args, **kwargs):
        messages.success(self.request, 'Вы разлогинены')
        return super().dispatch(request, *args, **kwargs)