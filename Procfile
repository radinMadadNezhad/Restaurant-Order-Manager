release: python manage.py migrate --noinput
web: gunicorn restaurant_management.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 60 