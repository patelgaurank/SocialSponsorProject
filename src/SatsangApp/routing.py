# mysite/routing.py
import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import include, url
from django.urls import path, re_path

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SatsangApp.settings")
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()
from sponsorApp import consumers

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    # Django's ASGI application to handle traditional HTTP requests
    "http": django_asgi_app,
        
    'websocket': AuthMiddlewareStack(
        URLRouter(
            [
                re_path('', consumers.alertMessage.as_asgi()),
                re_path(r'^sponsorApp/dashboard/$', consumers.alertMessage.as_asgi()),
                re_path(r'^sponsorApp/sponsorform/$', consumers.alertMessage.as_asgi()),
                re_path(r'^sponsorApp/sponsordata/$', consumers.alertMessage.as_asgi()),
                re_path(r'^accounts/', consumers.alertMessage.as_asgi()),
                re_path(r'^ims/imsdata/$', consumers.alertMessage.as_asgi()),
                re_path(r'^ims/imsform/$', consumers.alertMessage.as_asgi()),
                re_path(r'^sponsorApp/purposecode/$', consumers.alertMessage.as_asgi()),
                re_path(r'^sponsorApp/team/$', consumers.alertMessage.as_asgi()),
                re_path(r'^sponsorApp/display/$', consumers.alertMessage.as_asgi()),
            ]
        )
    ),
})