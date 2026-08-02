import os
import django
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# S'assurer que le registre des applications est bien chargé
django.setup()

application = get_wsgi_application()
