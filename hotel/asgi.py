"""
ASGI config for hotel project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path, re_path
from pizza import consumers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel.settings')

application = get_asgi_application()

ws_patterns=[
    path('test/', consumers.MyConsumer.as_asgi()),
    path("ws/pizza/<order_id>/", consumers.OrderProgess.as_asgi())
]

application= ProtocolTypeRouter({
    'websocket':AuthMiddlewareStack(URLRouter(ws_patterns))
})


