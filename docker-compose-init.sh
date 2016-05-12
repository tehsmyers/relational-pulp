#!/bin/sh

# Once the DB is up, populate the DB and regenerate the search index

until psql -h db -U pulp -c '\conninfo'
do
    sleep 5
done

until curl http://search:9200/;
do
    sleep 5
done

python manage.py migrate --run-syncdb
cat populate.py | python manage.py shell >/dev/null
python manage.py update_index -r

echo "Starting webserver"
python manage.py runserver 0.0.0.0:8000
