#!/bin/sh

if [ "$DB_HOST" = "db" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DB_HOST $DB_PORT; do
        sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py collectstatic
python manage.py migrate

exec "$@"
