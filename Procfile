web: python manage.py runserver 0.0.0.0:8000
worker: celery -A soundbooth worker -l debug -S django
beat: celery -A soundbooth beat -l debug -S django
