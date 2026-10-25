#!/usr/bin/env bash
# Render: Start Command -> ./start.sh
# migrate shu yerda, chunki Render doimiy diski build paytida ulanmagan bo'ladi.
set -o errexit
mkdir -p "${PRIVATE_MEDIA_ROOT:-private_media}"
python manage.py migrate --noinput

# Admin: Environment'da DJANGO_SUPERUSER_USERNAME va DJANGO_SUPERUSER_PASSWORD berilsa,
# birinchi ishga tushishda bir marta yaratiladi (bor bo'lsa, tegilmaydi).
if [ -n "${DJANGO_SUPERUSER_USERNAME:-}" ] && [ -n "${DJANGO_SUPERUSER_PASSWORD:-}" ]; then
  python manage.py shell -c "
from django.contrib.auth import get_user_model
import os
U = get_user_model(); n = os.environ['DJANGO_SUPERUSER_USERNAME']
if not U.objects.filter(username=n).exists():
    U.objects.create_superuser(n, os.environ.get('DJANGO_SUPERUSER_EMAIL', ''), os.environ['DJANGO_SUPERUSER_PASSWORD'])
    print('Admin yaratildi:', n)
"
fi
exec gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2 --timeout 60
