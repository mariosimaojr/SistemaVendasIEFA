from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import CharField, Q
from django.db.models.functions import Cast
from django.utils import timezone

from .models import MovimentacaoEstoque
from .forms import MovimentacaoEstoqueForm


def lista(request):

    q = request.GET.get('q', '').strip()

    movimentacoes = MovimentacaoEstoque.objects.select_related(
        'produto',
        'produto__categoria'
    ).annotate(
        sequencia_texto=Cast(
            'sequencia',
            output_field=CharField()
        ),
        produto_sequencia_texto=Cast(
            'produto__sequencia',
            output_field=CharField()
        )
    ).order_by('-sequencia')

    if q:
        filtros = (
            Q(sequencia_texto__icontains=q) |
            Q(produto_sequencia_texto__icontains=q) |
            Q(produto__nome__icontains=q) |
            Q(produto__descricao__icontains=q) |
            Q(produto__categoria__nome__icontains=q) |
            Q(produto__categoria__descricao__icontains=q)
        )

        if q.isdigit():
            filtros |= (
                Q(sequencia=int(q)) |
                Q(produto__sequencia=int(q))
            )

        movimentacoes = movimentacoes.filter(filtros)

    return render(
        request,
        'movimentacoes_estoque/lista.html',
        {
            'movimentacoes': movimentacoes,
            'q': q
        }
    )


def criar(request):

    if request.method == 'POST':

        form = MovimentacaoEstoqueForm(request.POST)

        if form.is_valid():

            movimentacao = form.save(commit=False)
            movimentacao.usuario = request.usuario_logado

            if not movimentacao.data_movimento:
                movimentacao.data_movimento = timezone.now()

            quantidade = abs(movimentacao.quantidade)

            if movimentacao.tipo_movimento == 'ENTRADA':
                movimentacao.quantidade = quantidade
            else:
                movimentacao.quantidade = -quantidade

            movimentacao.save()

            return redirect('movimentacoes_estoque:lista')

    else:

        form = MovimentacaoEstoqueForm(
            initial={
                'data_movimento': timezone.now().strftime('%Y-%m-%dT%H:%M'),
                'tipo_movimento': 'ENTRADA'
            }
        )

    return render(
        request,
        'movimentacoes_estoque/form.html',
        {
            'form': form,
            'titulo': 'Nova Movimentação de Estoque'
        }
    )


def editar(request, pk):

    movimentacao = get_object_or_404(
        MovimentacaoEstoque,
        pk=pk
    )

    if request.method == 'POST':

        form = MovimentacaoEstoqueForm(
            request.POST,
            instance=movimentacao
        )

        if form.is_valid():

            movimentacao = form.save(commit=False)

            quantidade = abs(movimentacao.quantidade)

            if movimentacao.tipo_movimento == 'ENTRADA':
                movimentacao.quantidade = quantidade
            else:
                movimentacao.quantidade = -quantidade

            movimentacao.save()

            return redirect('movimentacoes_estoque:lista')

    else:

        movimentacao_inicial = movimentacao
        movimentacao_inicial.quantidade = abs(movimentacao.quantidade)

        form = MovimentacaoEstoqueForm(
            instance=movimentacao_inicial
        )

    return render(
        request,
        'movimentacoes_estoque/form.html',
        {
            'form': form,
            'titulo': 'Editar Movimentação de Estoque'
        }
    )


def excluir(request, pk):

    movimentacao = get_object_or_404(
        MovimentacaoEstoque,
        pk=pk
    )

    movimentacao.delete()

    return redirect('movimentacoes_estoque:lista')
