from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import urlencode

from .auth import get_usuario_logado, logout_usuario


class UsuarioLogadoMiddleware:

    def __init__(self, get_response):

        self.get_response = get_response

    def __call__(self, request):

        request.usuario_logado = get_usuario_logado(request)

        if self._rota_publica(request):
            return self.get_response(request)

        if request.usuario_logado is None:
            logout_usuario(request)

            login_url = reverse('login')
            query_string = urlencode({'next': request.get_full_path()})

            return redirect(f'{login_url}?{query_string}')

        return self.get_response(request)

    def _rota_publica(self, request):

        login_url = reverse('login')
        logout_url = reverse('logout')

        return (
            request.path == login_url or
            request.path == logout_url or
            request.path.startswith('/static/')
        )
