from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import Produto
from .forms import ProdutoForm


def lista(request):

    produtos = Produto.objects.select_related('categoria').all()

    return render(
        request,
        'produtos/lista.html',
        {
            'produtos': produtos
        }
    )


def criar(request):

    if request.method == 'POST':

        form = ProdutoForm(request.POST)

        if form.is_valid():

            produto = form.save(commit=False)
            produto.data_cadastro = timezone.now()
            produto.save()

            return redirect('produtos:lista')

    else:

        form = ProdutoForm()

    return render(
        request,
        'produtos/form.html',
        {
            'form': form,
            'titulo': 'Novo Produto'
        }
    )


def editar(request, pk):

    produto = get_object_or_404(
        Produto,
        pk=pk
    )

    if request.method == 'POST':

        form = ProdutoForm(
            request.POST,
            instance=produto
        )

        if form.is_valid():

            produto = form.save(commit=False)

            if not produto.data_cadastro:
                produto.data_cadastro = timezone.now()

            produto.save()

            return redirect('produtos:lista')

    else:

        form = ProdutoForm(
            instance=produto
        )

    return render(
        request,
        'produtos/form.html',
        {
            'form': form,
            'titulo': 'Editar Produto'
        }
    )


def excluir(request, pk):

    produto = get_object_or_404(
        Produto,
        pk=pk
    )

    produto.delete()

    return redirect('produtos:lista')