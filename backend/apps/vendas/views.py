from decimal import Decimal

from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from apps.produtos.models import Produto
from .forms import VendaForm, criar_venda_item_formset
from .models import Venda


def lista(request):

    vendas = Venda.objects.select_related(
        'usuario',
        'forma_pagamento'
    ).all()

    return render(
        request,
        'vendas/lista.html',
        {
            'vendas': vendas
        }
    )


@transaction.atomic
def criar(request):

    VendaItemFormSet = criar_venda_item_formset(extra=3)

    if request.method == 'POST':

        form = VendaForm(request.POST)
        formset = VendaItemFormSet(request.POST)

        if form.is_valid() and formset.is_valid():

            venda = form.save(commit=False)
            venda.valor_total = Decimal('0.00')
            venda.save()

            total = Decimal('0.00')

            for item_form in formset:
                if not item_form.cleaned_data or item_form.cleaned_data.get('DELETE'):
                    continue

                produto = item_form.cleaned_data.get('produto')
                quantidade = item_form.cleaned_data.get('quantidade')
                preco_unitario = item_form.cleaned_data.get('preco_unitario')

                if not (produto and quantidade and preco_unitario):
                    continue

                item = item_form.save(commit=False)
                item.venda = venda
                item.subtotal = item.quantidade * item.preco_unitario
                total += item.subtotal
                item.save()

            venda.valor_total = total
            venda.save()

            return redirect('vendas:lista')

    else:

        form = VendaForm(
            initial={
                'data_venda': timezone.localdate()
            }
        )
        formset = VendaItemFormSet()

    return render(
        request,
        'vendas/form.html',
        {
            'form': form,
            'formset': formset,
            'titulo': 'Nova Venda'
        }
    )


@transaction.atomic
def editar(request, pk):

    venda = get_object_or_404(Venda, pk=pk)

    itens_queryset = venda.itens.all().order_by('sequencia')

    quantidade_itens = itens_queryset.count()
    extra = max(0, 3 - quantidade_itens)

    VendaItemFormSet = criar_venda_item_formset(extra=extra)

    if request.method == 'POST':

        form = VendaForm(
            request.POST,
            instance=venda
        )

        formset = VendaItemFormSet(
            request.POST,
            instance=venda,
            queryset=itens_queryset
        )

        if form.is_valid() and formset.is_valid():

            venda = form.save(commit=False)
            venda.save()

            itens = formset.save(commit=False)

            for obj in formset.deleted_objects:
                obj.delete()

            for item in itens:
                produto = getattr(item, 'produto', None)
                quantidade = getattr(item, 'quantidade', None)
                preco_unitario = getattr(item, 'preco_unitario', None)

                if not (produto and quantidade and preco_unitario):
                    continue

                item.venda = venda
                item.subtotal = item.quantidade * item.preco_unitario
                item.save()

            total = Decimal('0.00')

            for item in venda.itens.all():
                total += item.subtotal or Decimal('0.00')

            venda.valor_total = total
            venda.save()

            return redirect('vendas:lista')

    else:

        form = VendaForm(instance=venda)

        formset = VendaItemFormSet(
            instance=venda,
            queryset=itens_queryset
        )

    return render(
        request,
        'vendas/form.html',
        {
            'form': form,
            'formset': formset,
            'titulo': 'Editar Venda'
        }
    )

def excluir(request, pk):

    venda = get_object_or_404(
        Venda,
        pk=pk
    )

    venda.delete()

    return redirect('vendas:lista')


def buscar_produto(request):

    codigo = request.GET.get('codigo')

    if not codigo:
        return JsonResponse(
            {
                'ok': False,
                'mensagem': 'Código não informado.'
            }
        )

    try:
        produto = Produto.objects.get(
            sequencia=codigo,
            ativo=True
        )

        return JsonResponse(
            {
                'ok': True,
                'sequencia': produto.sequencia,
                'nome': produto.nome,
                'preco_venda': float(produto.preco_venda),
            }
        )

    except Produto.DoesNotExist:
        return JsonResponse(
            {
                'ok': False,
                'mensagem': 'Produto não encontrado.'
            }
        )