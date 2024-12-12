import os
from django.core.wsgi import get_wsgi_application

# Ensure this is consistent with your Azure settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()
