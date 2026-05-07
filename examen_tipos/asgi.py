import os
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "examen_tipos.settings")
application = get_asgi_application()
