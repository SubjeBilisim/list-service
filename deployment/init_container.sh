#!/bin/sh

cd /app/src

python manage.py collectstatic --no-input
export DJANGO_SETTINGS_MODULE=social_list_service.settings.prod

gunicorn provider.wsgi --config /app/deployment/gunicorn_config.py
