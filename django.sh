#!/bin/sh

# Attendre que la base de données soit prête
echo "Waiting for database..."
while ! nc -z mydb 3306; do
  sleep 0.1
done

# Exécuter les migrations
echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate

# Démarrer le serveur
echo "Starting server..."
python manage.py runserver 0.0.0.0:8000
