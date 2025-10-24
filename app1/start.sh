#!/bin/sh

python manage.py makemigrations
python manage.py migrate

# collects all static files in our app and puts it in the STATIC_ROOT
python manage.py collectstatic --noinput

gunicorn --worker-tmp-dir /dev/shm "app1.wsgi" -b :5000 --timeout 60 -w 4
