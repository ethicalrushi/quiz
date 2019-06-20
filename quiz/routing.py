from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

from quizapp.consumers import ChatConsumer

application = ProtocolTypeRouter({
    'websocket':AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                    url(r'^quiz/quesn/$', ChatConsumer),
                ]
            )
        )
    )
})