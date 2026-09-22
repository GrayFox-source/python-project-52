from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect

from .models import Status
from .forms import StatusForm

# Create your views here.


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/index.html'
    context_object_name = 'statuses'
    login_url = '/login/'


class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('statuses:index')
    login_url = '/login/'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Статус успешно создан')
        return response


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/update.html'
    success_url = reverse_lazy('statuses:index')
    login_url = '/login/'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Статус успешно изменен')
        return response


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('statuses:index')
    login_url = '/login/'

    def delete(self, request, *args, **kwargs):
        status = self.get_object()

        # В будущем здесь будет проверка: if status.tasks.exists():
        #     messages.error(request, 'Невозможно удалить статус')
        #     return redirect('statuses:index')

        messages.success(self.request, 'Статус успешно удален')
        return super().delete(request, *args, **kwargs)
