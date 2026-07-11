from .models import Usuario


USUARIO_SESSION_KEY = 'usuario_logado_id'


def login_usuario(request, usuario):

    request.session.flush()
    request.session[USUARIO_SESSION_KEY] = usuario.sequencia


def logout_usuario(request):

    request.session.flush()


def get_usuario_logado(request):

    usuario_id = request.session.get(USUARIO_SESSION_KEY)

    if not usuario_id:
        return None

    try:
        return Usuario.objects.get(
            sequencia=usuario_id,
            ativo=True
        )
    except Usuario.DoesNotExist:
        return None
