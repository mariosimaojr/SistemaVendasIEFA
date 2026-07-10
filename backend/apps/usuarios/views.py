from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme

from .models import Usuario
from .forms import LoginForm, UsuarioForm
import hashlib
from django.utils import timezone


def login_view(request):

    next_url = request.GET.get('next') or request.POST.get('next') or ''

    if request.method == 'GET' and getattr(request, 'usuario_logado', None):
        return redirect(_destino_login(request, next_url))

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            login_acesso = form.cleaned_data['login_acesso']
            senha = form.cleaned_data['senha']
            senha_hash = hashlib.sha1(senha.encode()).hexdigest()

            usuario = Usuario.objects.filter(
                login_acesso=login_acesso,
                senha_hash=senha_hash,
                ativo=True
            ).first()

            if usuario is None:
                form.add_error(
                    None,
                    'Login ou senha invalidos.'
                )
            else:
                from .auth import login_usuario

                login_usuario(request, usuario)

                return redirect(_destino_login(request, next_url))
    else:
        form = LoginForm()

    return render(
        request,
        'usuarios/login.html',
        {
            'form': form,
            'next': next_url
        }
    )


def logout_view(request):

    from .auth import logout_usuario

    logout_usuario(request)

    return redirect('login')


def _destino_login(request, next_url):

    if next_url and url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure()
    ):
        return next_url

    return reverse('home')


def lista(request):
    usuarios = Usuario.objects.all()
    return render(
        request,
        'usuarios/lista.html',
        {
            'usuarios': usuarios
        }
    )

def criar(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            senha = form.cleaned_data['senha']
            senha_hash = hashlib.sha1(
               senha.encode()
           ).hexdigest()
            usuario.senha_hash = senha_hash
            usuario.data_criacao = timezone.now()
            usuario.save()
            return redirect('usuarios:lista')
    else:
        form = UsuarioForm()
    return render(
        request,
        'usuarios/form.html',
        {
            'form': form
        }
    )

def editar(request, pk):
    usuario = get_object_or_404(
        Usuario,
        pk=pk
    )
    if request.method == 'POST':
        form = UsuarioForm(
            request.POST,
            instance=usuario
        )
        if form.is_valid():
            usuario = form.save(commit=False)

            senha = form.cleaned_data.get('senha')
            if senha:
                senha_hash = hashlib.sha1(senha.encode()).hexdigest()
                usuario.senha_hash = senha_hash
            usuario.save()
            
            return redirect('usuarios:lista')
    else:
        form = UsuarioForm(
            instance=usuario
        )
    return render(
        request,
        'usuarios/form.html',
        {
            'form': form
        }
    )

def excluir(request, pk):

    usuario = get_object_or_404(
        Usuario,
        pk=pk
    )

    usuario.delete()

    return redirect('usuarios:lista')
