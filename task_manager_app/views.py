from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
     return render(request, 'index.html')

def test_error(request):  # <-- ДОБАВИТЬ
    """Временная функция для тестирования Sentry"""
    raise Exception("Тестовая ошибка для проверки Bugsink - можно удалить после проверки")