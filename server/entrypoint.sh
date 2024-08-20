#!/bin/sh

# Make migrations and migrate the database.
echo "Making migrations and migrating the database. "
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput
export DJANGO_SUPERUSER_USERNAME=rule1
export DJANGO_SUPERUSER_PASSWORD=stol67812
export DJANGO_SUPERUSER_EMAIL="root@root.com"
python manage.py createsuperuser --noinput


exec "$@"