#!/bin/bash -x

# This assumes you're running in vagrant.
echo "drop database pulp; create database pulp owner pulp" | sudo -u postgres psql

rm -rf pulp/migrations pulp_rpm/migrations
rm -rf content

python manage.py makemigrations pulp --noinput
python manage.py makemigrations pulp_rpm --noinput

./db-init.sh
