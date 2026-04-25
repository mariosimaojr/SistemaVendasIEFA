from django.shortcuts import render, redirect, get_object_or_404

from .models import Categoria
from .forms import CategoriaForm


def lista_categorias(request):

    categorias = Categoria.objects.all().order_by(
        '-sequencia'
    )

    return render(
        request,
        'categorias/lista.html',
        {
            'categorias': categorias
        }
    )


def nova_categoria(request):

    if request.method == 'POST':

        form = CategoriaForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            return redirect(
                'categorias:lista'
            )

    else:

        form = CategoriaForm()

    return render(
        request,
        'categorias/form.html',
        {
            'form': form
        }
    )


def editar_categoria(request, id):

    categoria = get_object_or_404(
        Categoria,
        sequencia=id
    )

    if request.method == 'POST':

        form = CategoriaForm(
            request.POST,
            instance=categoria
        )

        if form.is_valid():

            form.save()

            return redirect(
                'categorias:lista'
            )

    else:

        form = CategoriaForm(
            instance=categoria
        )

    return render(
        request,
        'categorias/form.html',
        {
            'form': form
        }
    )


def excluir_categoria(request, id):

    categoria = get_object_or_404(
        Categoria,
        sequencia=id
    )

    categoria.delete()

    return redirect('categorias:lista')