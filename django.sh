#!/bin/sh

# Attendre que la base de données soit prête
while ! nc -z $PG_HOST $PG_PORT; do
  sleep 0.1
done

# Faire les migrations
python manage.py makemigrations
python manage.py migrate

# Lancer le serveur
exec "$@"
