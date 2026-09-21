.PHONY: install tailwind-build collectstatic migrate setup build render-start dev

install:
	uv sync

tailwind-build:
	uv run python manage.py tailwind build

collectstatic:
	uv run python manage.py collectstatic --noinput

migrate:
	uv run python manage.py migrate

# ВАЖНО: tailwind-build должен идти СТРОГО ПЕРЕД collectstatic
setup: install tailwind-build collectstatic migrate

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi:application

# Для локальной разработки лучше использовать эту команду, она следит за изменениями
dev:
	uv run python manage.py tailwind runserver