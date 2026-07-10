from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import MovimentacaoEstoque
from .forms import MovimentacaoEstoqueForm


def lista(request):

    movimentacoes = MovimentacaoEstoque.objects.select_related(
        'produto',
        'usuario'
    ).all()

    return render(
        request,
        'movimentacoes_estoque/lista.html',
        {
            'movimentacoes': movimentacoes
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
