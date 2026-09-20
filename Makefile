.PHONY: install collectstatic migrate setup build render-start dev

install:
	uv sync

collectstatic:
	uv run python manage.py collectstatic --noinput

migrate:
	uv run python manage.py migrate

setup: install collectstatic migrate

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi:application

dev:
	uv run python manage.py runserver