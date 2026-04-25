from django.shortcuts import render, redirect, get_object_or_404
from .models import Usuario
from .forms import UsuarioForm
import hashlib
from django.utils import timezone

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