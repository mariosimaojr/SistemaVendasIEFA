from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.db.models import Q, Sum
from django.db.models.functions import Coalesce
from django.urls import reverse
from django.utils import timezone

from apps.movimentacoes_estoque.models import MovimentacaoEstoque

from .models import Produto
from .forms import ProdutoForm


def lista(request):

    q = request.GET.get('q', '').strip()

    produtos = Produto.objects.select_related('categoria').annotate(
        estoque_atual=Coalesce(
            Sum('movimentacaoestoque__quantidade'),
            0
        )
    )

    if q:
        produtos = produtos.filter(
            Q(nome__icontains=q) |
            Q(categoria__nome__icontains=q)
        )

    return render(
        request,
        'produtos/lista.html',
        {
            'produtos': produtos,
            'q': q
        }
    )


def criar(request):

    produto_criado = request.GET.get('produto_criado')

    if request.method == 'POST':

        form = ProdutoForm(
            request.POST,
            is_create=True
        )

        if form.is_valid():

            estoque_inicial = form.cleaned_data['estoque_inicial']
            usuario_estoque = form.cleaned_data['usuario_estoque']

            with transaction.atomic():

                produto = form.save(commit=False)
                produto.data_cadastro = timezone.now()
                produto.save()

                if estoque_inicial > 0:
                    MovimentacaoEstoque.objects.create(
                        produto=produto,
                        quantidade=estoque_inicial,
                        data_movimento=timezone.now(),
                        observacao='Estoque inicial informado no cadastro do produto.',
                        usuario=usuario_estoque,
                        tipo_movimento='ENTRADA'
                    )

            return redirect(
                f"{reverse('produtos:novo')}?produto_criado={produto.sequencia}"
            )

    else:

        form = ProdutoForm(
            is_create=True
        )

    return render(
        request,
        'produtos/form.html',
        {
            'form': form,
            'titulo': 'Novo Produto',
            'produto_criado': produto_criado
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
