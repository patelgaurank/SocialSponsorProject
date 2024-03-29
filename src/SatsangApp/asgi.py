"""
ASGI config for SatsangApp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

import django
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.http import AsgiHandler
from django.core.asgi import get_asgi_application
from . import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SatsangApp.settings')
django.setup()

application = ProtocolTypeRouter({
    # "http": AsgiHandler(),
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
            URLRouter(
                routing.websocket_urlpatterns
            )
        ),    
})
