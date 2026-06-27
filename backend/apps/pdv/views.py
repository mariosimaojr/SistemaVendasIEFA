from collections import defaultdict
from decimal import Decimal

from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone

from apps.produtos.models import Produto
from apps.vendas.models import Venda, VendaItem

from .forms import PdvVendaForm


def caixa(request):

    if request.method == 'POST':

        form = PdvVendaForm(request.POST)

        if form.is_valid():

            itens = _agrupar_itens(form.cleaned_data['itens_json'])
            produtos = Produto.objects.filter(
                sequencia__in=itens.keys(),
                ativo=True
            ).in_bulk()

            produtos_faltantes = [
                str(produto_id)
                for produto_id in itens.keys()
                if produto_id not in produtos
            ]

            if produtos_faltantes:
                form.add_error(
                    'itens_json',
                    'Produto nao encontrado ou inativo: ' + ', '.join(produtos_faltantes)
                )
            else:
                venda = _salvar_venda_pdv(form, itens, produtos)

                messages.success(
                    request,
                    f'Venda #{venda.sequencia} finalizada com sucesso.'
                )

                return redirect('pdv:caixa')

    else:

        form = PdvVendaForm()

    return render(
        request,
        'pdv/caixa.html',
        {
            'form': form,
        }
    )


def buscar_produto(request):

    codigo = request.GET.get('codigo', '').strip()

    if not codigo:
        return JsonResponse(
            {
                'ok': False,
                'mensagem': 'Codigo nao informado.',
            }
        )

    try:
        produto = Produto.objects.get(
            sequencia=codigo,
            ativo=True
        )
    except Produto.DoesNotExist:
        return JsonResponse(
            {
                'ok': False,
                'mensagem': 'Produto nao encontrado.',
            }
        )

    return JsonResponse(
        {
            'ok': True,
            'sequencia': produto.sequencia,
            'codigo': str(produto.sequencia).zfill(4),
            'nome': produto.nome,
            'preco_venda': str(produto.preco_venda),
        }
    )


def _agrupar_itens(itens):

    itens_agrupados = defaultdict(int)

    for item in itens:
        itens_agrupados[item['produto_id']] += item['quantidade']

    return itens_agrupados


@transaction.atomic
def _salvar_venda_pdv(form, itens, produtos):

    venda = Venda.objects.create(
        data_venda=timezone.localdate(),
        usuario=form.cleaned_data['usuario'],
        forma_pagamento=form.cleaned_data['forma_pagamento'],
        valor_total=Decimal('0.00'),
        observacao=None
    )

    valor_total = Decimal('0.00')

    for produto_id, quantidade in itens.items():
        produto = produtos[produto_id]
        preco_unitario = produto.preco_venda
        subtotal = preco_unitario * quantidade

        VendaItem.objects.create(
            venda=venda,
            produto=produto,
            quantidade=quantidade,
            preco_unitario=preco_unitario,
            subtotal=subtotal
        )

        valor_total += subtotal

    venda.valor_total = valor_total
    venda.save(update_fields=['valor_total'])

    return venda
