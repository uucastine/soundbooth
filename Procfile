web: python manage.py runserver 0.0.0.0:8000
worker: celery -A soundbooth worker
beat: celery -A soundbooth beat -S django
