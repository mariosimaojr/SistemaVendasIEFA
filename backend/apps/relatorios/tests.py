from datetime import date
from decimal import Decimal
from unittest.mock import patch

from django.shortcuts import render as django_render
from django.test import RequestFactory, SimpleTestCase

from .views import vendas_forma_pagamento


class ResumoPeriodoTests(SimpleTestCase):
    def gerar(self, inicio, fim, vendas=(), produtos=()):
        request = RequestFactory().get('/', {'data_inicial': inicio, 'data_final': fim})
        with (
            patch('apps.relatorios.views.Venda.objects.filter') as vendas_filter,
            patch('apps.relatorios.views.VendaItem.objects.filter') as itens_filter,
            patch('apps.relatorios.views.render', wraps=django_render) as render_mock,
        ):
            vendas_filter.return_value.values.return_value.annotate.return_value.order_by.return_value = vendas
            itens_filter.return_value.values.return_value.annotate.return_value.order_by.return_value = produtos
            response = vendas_forma_pagamento(request)
            context = render_mock.call_args.args[2]
            if context['form'].is_valid():
                vendas_filter.assert_called_once_with(
                    data_venda__gte=date.fromisoformat(inicio),
                    data_venda__lte=date.fromisoformat(fim),
                )
                itens_filter.assert_called_once()
            else:
                vendas_filter.assert_not_called()
                itens_filter.assert_not_called()
        return response, context

    def venda(self, dia, forma, valor):
        return {'data_venda': date(2026, 10, dia),
                'forma_pagamento__descricao': forma, 'valor_total': Decimal(valor)}

    def test_consolidado_soma_formas_e_preserva_detalhes(self):
        vendas = [self.venda(25, 'PIX', '10.10'), self.venda(25, 'DINHEIRO', '20.00'),
                  self.venda(26, 'PIX', '5.25'), self.venda(26, 'CARTÃO', '30.00')]
        produtos = [{'venda__data_venda': date(2026, 10, 25),
                     'produto__nome': 'Livro', 'quantidade_total': 2}]
        response, context = self.gerar('2026-10-25', '2026-10-26', vendas, produtos)
        self.assertEqual(context['resumo_periodo'], [
            {'forma_pagamento': 'CARTÃO', 'valor_total': Decimal('30.00')},
            {'forma_pagamento': 'DINHEIRO', 'valor_total': Decimal('20.00')},
            {'forma_pagamento': 'PIX', 'valor_total': Decimal('15.35')},
        ])
        blocos = context['relatorio']
        self.assertEqual([b['total_geral'] for b in blocos], [Decimal('30.10'), Decimal('35.25')])
        self.assertEqual(context['total_periodo'], Decimal('65.35'))
        self.assertEqual(context['total_periodo'], sum(b['total_geral'] for b in blocos))
        self.assertEqual(blocos[0]['produtos'], [{'produto': 'Livro', 'quantidade': 2}])
        self.assertEqual(blocos[1]['produtos'], [])
        self.assertEqual(blocos[0]['resumo'][0]['valor_total'], Decimal('10.10'))
        self.assertContains(response, 'TOTAL GERAL', count=3)
        html = response.content.decode()
        self.assertLess(html.index('Resumo do período'), html.index('Data: 25/10/2026'))

    def test_um_dia_sem_consolidado(self):
        response, context = self.gerar('2026-10-25', '2026-10-25', [self.venda(25, 'PIX', '10.00')])
        self.assertEqual(context['resumo_periodo'], [])
        self.assertNotContains(response, 'Resumo do período')
        self.assertContains(response, 'TOTAL GERAL', count=1)

    def test_intervalo_com_vendas_em_apenas_um_dia(self):
        response, context = self.gerar('2026-10-25', '2026-10-27', [self.venda(25, 'PIX', '10.00')])
        self.assertContains(response, 'Resumo do período')
        self.assertEqual(context['total_periodo'], Decimal('10.00'))
        self.assertEqual(len(context['relatorio']), 1)

    def test_sem_resultados(self):
        response, context = self.gerar('2026-10-25', '2026-10-27')
        self.assertEqual(context['resumo_periodo'], [])
        self.assertNotContains(response, 'Resumo do período')
        self.assertContains(response, 'Nenhum dado encontrado para o período informado.')

    def test_datas_invalidas(self):
        for inicio, fim in [('2026-10-27', '2026-10-25'), ('invalida', '2026-10-27'), ('2026-10-25', '')]:
            with self.subTest(inicio=inicio, fim=fim):
                response, context = self.gerar(inicio, fim)
                self.assertTrue(context['form'].errors)
                self.assertEqual(context['relatorio'], [])
                self.assertNotContains(response, 'Resumo do período')
