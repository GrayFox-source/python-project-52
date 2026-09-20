#!/usr/bin/env bash
set -e

# Скачиваем uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Добавляем uv в PATH
source $HOME/.local/bin/env || true

# Устанавливаем зависимости
uv sync

# Собираем статику
uv run python manage.py collectstatic --noinput

# Применяем миграции
uv run python manage.py migrate

echo "Build completed successfully"