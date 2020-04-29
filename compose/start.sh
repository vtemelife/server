#!/bin/sh
set -e
python manage.py collectstatic --noinput
python manage.py migrate --noinput
python manage.py compilemessages --locale ru
uwsgi --ini ./compose/uwsgi.ini
