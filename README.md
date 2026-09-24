# Менеджер задач (Python)

[![hexlet-check](https://github.com/GrayFox-source/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/GrayFox-source/python-project-52/actions)

На практике узнаете о проектировании баз данных, PaaS, мониторинге ошибок, ORM, фреймворке Django, шаблонизации и Tailwind CSS.

Учебный проект Хекслета: https://ru.hexlet.io/programs/python  
**Демонстрация работы проекта:** https://python-project-52-scbm.onrender.com

## Стек

- Python 3.12+
- Django
- uv (менеджер пакетов и виртуальных окружений)
- Tailwind CSS (через `django-tailwind-cli`)
- PostgreSQL (в продакшене) / SQLite (локально)
- Sentry/Bugsink (мониторинг ошибок)

## Установка и запуск

1. Клонируйте репозиторий и перейдите в директорию проекта:
```bash
git clone https://github.com/GrayFox-source/python-project-52.git
cd python-project-52
```
2. Установите зависимости с помощью uv:
```bash
uv sync
```
3. Создайте файл .env в корне проекта и добавьте необходимые переменные окружения (пример):
```bash
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
SENTRY_DSN=your-sentry-dsn-here
```
4. Примените миграции базы данных:
```bash
uv run python manage.py migrate
```
5. Соберите статические файлы Tailwind CSS:
```bash
uv run python manage.py tailwind build
```
6. Запустите сервер разработки (с автоматической пересборкой стилей):
```bash
uv run python manage.py tailwind runserver
```
Приложение будет доступно по адресу: http://127.0.0.1:8000

# **Тестирование**

Для запуска автоматических тестов используйте команду:
```bash
uv run python manage.py test
```

<details>
<summary>Автоматические тесты Хекслета</summary>

Тесты запускаются на каждый коммит. За запуск отвечает файл .github/workflows/hexlet-check.yml — не удаляйте и не переименовывайте ни его, ни репозиторий.
</details>

О Хекслете
Хекслет — школа программирования: авторские программы обучения с практикой, поддержкой наставников и реальными проектами, которые остаются в резюме. Этот репозиторий — один из таких проектов.