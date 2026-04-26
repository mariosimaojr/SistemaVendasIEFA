# apps/relatorios/views.py
from collections import defaultdict
from decimal import Decimal

from django.db.models import Sum
from django.db.models.functions import TruncDate
from django.shortcuts import render

from apps.vendas.models import Venda, VendaItem
from .forms import RelatorioVendasFormaPagamentoForm

def lista(request):

    return render(
        request,
        'relatorios/lista.html'
    )


def codigo_barras(request):

    return render(
        request,
        'relatorios/codigo_barras.html'
    )


def vendas_forma_pagamento(request):

    form = RelatorioVendasFormaPagamentoForm(request.GET or None)

    relatorio = []
    data_inicial = None
    data_final = None

    if form.is_valid():

        data_inicial = form.cleaned_data['data_inicial']
        data_final = form.cleaned_data['data_final']

        resumo_queryset = (
            Venda.objects
            .filter(
                data_venda__gte=data_inicial,
                data_venda__lte=data_final
            )
            .values('data_venda', 'forma_pagamento__descricao')
            .annotate(valor_total=Sum('valor_total'))
            .order_by('data_venda', 'forma_pagamento__descricao')
        )

        produtos_queryset = (
            VendaItem.objects
            .filter(
                venda__data_venda__gte=data_inicial,
                venda__data_venda__lte=data_final
            )
            .values('venda__data_venda', 'produto__nome')
            .annotate(quantidade_total=Sum('quantidade'))
            .order_by('venda__data_venda', 'produto__nome')
        )

        agrupado = defaultdict(
            lambda: {
                'resumo': [],
                'produtos': [],
                'total_geral': Decimal('0.00')
            }
        )

        for item in resumo_queryset:

            data_ref = item['data_venda']
            forma = item['forma_pagamento__descricao']
            valor_total = item['valor_total'] or Decimal('0.00')

            agrupado[data_ref]['resumo'].append({
                'forma_pagamento': forma,
                'valor_total': valor_total,
            })

            agrupado[data_ref]['total_geral'] += valor_total

        for item in produtos_queryset:

            data_ref = item['venda__data_venda']
            produto = item['produto__nome']
            quantidade_total = item['quantidade_total'] or 0

            agrupado[data_ref]['produtos'].append({
                'produto': produto,
                'quantidade': quantidade_total,
            })

        relatorio = [
            {
                'data': data,
                'resumo': dados['resumo'],
                'produtos': dados['produtos'],
                'total_geral': dados['total_geral'],
            }
            for data, dados in sorted(agrupado.items())
        ]

    return render(
        request,
        'relatorios/vendas_forma_pagamento.html',
        {
            'form': form,
            'relatorio': relatorio,
            'data_inicial': data_inicial,
            'data_final': data_final,
        }
    )