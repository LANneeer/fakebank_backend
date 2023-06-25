import os
from celery import Celery
import django
# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bank.settings')
# Create a new Celery instance
celery_app = Celery('bank', include=['bank.tasks'])

# Load configuration from Django settings
celery_app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatically discover and register tasks in the "tasks" module
celery_app.autodiscover_tasks(related_name='tasks', packages=['payments'])
