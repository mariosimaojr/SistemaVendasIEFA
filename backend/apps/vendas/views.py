from decimal import Decimal
from datetime import datetime, time

from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import Venda, VendaItem
from .forms import VendaForm, VendaItemFormSet


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

    if request.method == 'POST':

        form = VendaForm(request.POST)
        formset = VendaItemFormSet(request.POST)

        if form.is_valid() and formset.is_valid():

            venda = form.save(commit=False)

            data_escolhida = form.cleaned_data['data_venda']
            venda.data_venda = datetime.combine(data_escolhida, time.min)

            venda.valor_total = Decimal('0.00')
            venda.save()

            total = Decimal('0.00')

            for item_form in formset:
                if not item_form.cleaned_data or item_form.cleaned_data.get('DELETE'):
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

    venda = get_object_or_404(
        Venda,
        pk=pk
    )

    if request.method == 'POST':

        form = VendaForm(
            request.POST,
            instance=venda
        )

        formset = VendaItemFormSet(
            request.POST,
            instance=venda
        )

        if form.is_valid() and formset.is_valid():

            venda = form.save(commit=False)

            data_escolhida = form.cleaned_data['data_venda']
            venda.data_venda = datetime.combine(data_escolhida, time.min)

            venda.valor_total = Decimal('0.00')
            venda.save()

            total = Decimal('0.00')

            itens = formset.save(commit=False)

            for obj in formset.deleted_objects:
                obj.delete()

            for item in itens:
                item.venda = venda
                item.subtotal = item.quantidade * item.preco_unitario
                total += item.subtotal
                item.save()

            venda.valor_total = total
            venda.save()

            return redirect('vendas:lista')

    else:

        form = VendaForm(
            instance=venda,
            initial={
                'data_venda': venda.data_venda.date() if venda.data_venda else None
            }
        )

        formset = VendaItemFormSet(instance=venda)

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

    if request.method == 'POST':
        venda.delete()
        return redirect('vendas:lista')

    return render(
        request,
        'vendas/excluir.html',
        {
            'venda': venda
        }
    )