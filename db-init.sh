#!/bin/sh

python manage.py migrate --noinput

echo -n 'import populate' | python manage.py shell
