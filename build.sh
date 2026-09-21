#!/usr/bin/env bash
set -e

# Скачиваем uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env || true

# Устанавливаем зависимости
uv sync

# 1. СНАЧАЛА собираем Tailwind стили!
uv run python manage.py tailwind build

# 2. ТОЛЬКО ПОТОМ собираем статику для WhiteNoise
uv run python manage.py collectstatic --noinput

# 3. Применяем миграции
uv run python manage.py migrate

echo "Build completed successfully"