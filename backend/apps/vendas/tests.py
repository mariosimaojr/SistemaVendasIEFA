from datetime import datetime
from types import SimpleNamespace
from unittest.mock import patch

from django.test import SimpleTestCase
from django.utils import timezone

from .services import registrar_baixa_estoque_venda_item


class RegistrarBaixaEstoqueVendaItemTests(SimpleTestCase):

    @patch('apps.vendas.services.MovimentacaoEstoque.objects.create')
    @patch('apps.vendas.services.timezone.now')
    def test_cria_movimentacao_de_saida_com_quantidade_negativa(
        self,
        timezone_now_mock,
        create_mock
    ):
        data_movimento = timezone.make_aware(datetime(2026, 8, 30, 10, 15))
        timezone_now_mock.return_value = data_movimento
        produto = SimpleNamespace(sequencia=7)
        usuario = SimpleNamespace(sequencia=2)
        item = SimpleNamespace(
            produto=produto,
            quantidade=3,
            venda_id=15,
            sequencia=9
        )

        registrar_baixa_estoque_venda_item(item, usuario)

        create_mock.assert_called_once_with(
            produto=produto,
            quantidade=-3,
            data_movimento=data_movimento,
            observacao='Baixa automática da venda #15 - item #9.',
            usuario=usuario,
            tipo_movimento='SAIDA'
        )
