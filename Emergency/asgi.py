"""
ASGI config for Emergency project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

from message.views import sio
import socketio
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Emergency.settings")
django_asgi_app = get_asgi_application()


application = socketio.ASGIApp(sio, django_asgi_app)
