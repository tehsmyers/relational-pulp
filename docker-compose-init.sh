#!/bin/sh

# Once the DB is up, populate the DB and regenerate the search index

until psql -h localhost -U pulp -c '\conninfo'
do
    sleep 5
done

# Django 1.9 handling (also holy crap Django this sort of change warrants 2.0)
# This assumes that syncdb will only fail if Django 1.9 is installed.
if python manage.py syncdb --noinput
then
    python manage.py migrate --noinput
else
    python manage.py migrate --run-syncdb
fi

cat populate.py | python manage.py shell >/dev/null

echo "Starting webserver"
python manage.py runserver 0.0.0.0:8000
